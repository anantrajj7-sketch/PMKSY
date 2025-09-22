"""Application views for PMKSY import workflows."""

from __future__ import annotations

import logging
from typing import Dict, Iterable, List, Tuple, Type

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views import View

from data_wizard import InputNeeded, registry as data_wizard_registry
from data_wizard.models import Run
from data_wizard.sources.models import FileSource

from .importers import REGISTRATIONS

logger = logging.getLogger(__name__)


PREVIEW_ERROR_MESSAGE = (
    "We couldn't read the uploaded file. Please upload a supported format."
)


class PreviewGenerationError(Exception):
    """Raised when a preview cannot be generated for an uploaded dataset."""


PREVIEW_LOAD_ERRORS: Tuple[Type[BaseException], ...] = (ValueError,)

try:  # pragma: no cover - optional dependency for XLS files
    from xlrd import XLRDError  # type: ignore
except ImportError:  # pragma: no cover - fallback when xlrd is unavailable
    XLRDError = None  # type: ignore[assignment]
else:  # pragma: no cover - exercised only when xlrd is installed
    PREVIEW_LOAD_ERRORS = PREVIEW_LOAD_ERRORS + (XLRDError,)

try:  # pragma: no cover - optional dependency for XLSX files
    from openpyxl.utils.exceptions import InvalidFileException
except ImportError:  # pragma: no cover - fallback when openpyxl is unavailable
    InvalidFileException = None  # type: ignore[assignment]
else:  # pragma: no cover - exercised only when openpyxl is installed
    PREVIEW_LOAD_ERRORS = PREVIEW_LOAD_ERRORS + (InvalidFileException,)

try:  # pragma: no cover - optional dependency used by data_wizard
    import itertable.exceptions as itertable_exceptions  # type: ignore
except ImportError:  # pragma: no cover - fallback when itertable is unavailable
    itertable_exceptions = None  # type: ignore[assignment]
else:  # pragma: no cover - exercised only when itertable is installed
    _itertable_error_types: List[Type[BaseException]] = []
    for name in ("TableError", "TableLoadError", "UnsupportedFormat"):
        exc = getattr(itertable_exceptions, name, None)
        if isinstance(exc, type) and issubclass(exc, BaseException):
            _itertable_error_types.append(exc)
    if _itertable_error_types:
        PREVIEW_LOAD_ERRORS = PREVIEW_LOAD_ERRORS + tuple(_itertable_error_types)


try:  # pragma: no cover - compatibility for future data_wizard releases
    from data_wizard.views import ImportWizard as BaseImportWizard  # type: ignore
except (ImportError, AttributeError):  # pragma: no cover - graceful fallback
    BaseImportWizard = View


class FileUploadForm(forms.Form):
    source_file = forms.FileField(
        label="Upload data file",
        help_text="Supported formats: CSV, XLSX, XLS, JSON",
    )


class ConfirmImportForm(forms.Form):
    run_id = forms.IntegerField(widget=forms.HiddenInput)


def build_wizard_registry() -> Dict[str, Dict[str, object]]:
    """Return a slug-indexed registry of configured importers."""

    registry: Dict[str, Dict[str, object]] = {}
    for name, serializer in REGISTRATIONS:
        slug = slugify(name)
        registry[slug] = {
            "name": name,
            "serializer": serializer,
        }
    return registry


WIZARD_MAP = build_wizard_registry()


def get_preview_rows(run: Run, limit: int = 5) -> Tuple[List[str], List[List[str]]]:
    """Generate a small preview of uploaded data for confirmation."""

    Loader = data_wizard_registry.get_loader(run.loader)
    loader = Loader(run)

    headers: List[str] = []
    rows: List[List[str]] = []

    try:
        table = loader.load_iter()

        if hasattr(table, "field_map") and table.field_map:
            headers = list(table.field_map.keys())

        iterator: Iterable = table
        for index, row in enumerate(iterator):
            if hasattr(row, "_asdict"):
                data = row._asdict()
            elif isinstance(row, dict):
                data = row
            elif isinstance(row, (list, tuple)):
                data = {str(i): value for i, value in enumerate(row)}
            else:
                data = {"value": row}

            if not headers:
                headers = list(data.keys())

            rows.append([str(data.get(column, "")) for column in headers])

            if index + 1 >= limit:
                break
    except PREVIEW_LOAD_ERRORS as exc:
        raise PreviewGenerationError("Unable to load preview data") from exc

    return headers, rows


class ImportHomeView(LoginRequiredMixin, View):
    template_name = "pmksy/home.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        wizards = [
            {
                "name": config["name"],
                "slug": slug,
            }
            for slug, config in WIZARD_MAP.items()
        ]
        context = {"wizards": wizards}
        return render(request, self.template_name, context)


class PMKSYImportWizard(LoginRequiredMixin, BaseImportWizard):
    upload_template_name = "pmksy/import_wizard_upload.html"
    preview_template_name = "pmksy/import_wizard_preview.html"
    success_template_name = "pmksy/wizard_done.html"

    form_class = FileUploadForm
    confirm_form_class = ConfirmImportForm

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.wizard_slug = kwargs.get("wizard_slug")
        if self.wizard_slug not in WIZARD_MAP:
            raise Http404("Unknown import wizard")
        self.wizard_config = WIZARD_MAP[self.wizard_slug]
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        run_id = request.GET.get("run")
        if run_id:
            run = self._get_user_run(run_id)
            try:
                headers, rows = get_preview_rows(run)
            except PreviewGenerationError:
                logger.exception("Failed to generate preview for run %s", run.pk)
                messages.error(request, PREVIEW_ERROR_MESSAGE)
                return redirect(
                    reverse("pmksy:wizard", kwargs={"wizard_slug": self.wizard_slug})
                )
            context = {
                "wizard": self.wizard_config,
                "run": run,
                "headers": headers,
                "rows": rows,
                "confirm_form": self.confirm_form_class(initial={"run_id": run.pk}),
            }
            return render(request, self.preview_template_name, context)

        context = {
            "wizard": self.wizard_config,
            "form": self.form_class(),
        }
        return render(request, self.upload_template_name, context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if "run_id" in request.POST:
            return self._handle_confirmation(request)
        return self._handle_upload(request)

    def _handle_upload(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            context = {"wizard": self.wizard_config, "form": form}
            return render(request, self.upload_template_name, context)

        uploaded_file = form.cleaned_data["source_file"]
        file_source = FileSource.objects.create(
            user=request.user,
            file=uploaded_file,
            name=f"{self.wizard_config['name']} Upload",
        )

        run = Run.objects.create(
            user=request.user,
            content_object=file_source,
            serializer=self.wizard_config["name"],
        )

        logger.info("Created run %s for wizard %s", run.pk, self.wizard_slug)

        return redirect(
            f"{reverse('pmksy:wizard', kwargs={'wizard_slug': self.wizard_slug})}?run={run.pk}"
        )

    def _handle_confirmation(self, request: HttpRequest) -> HttpResponse:
        form = self.confirm_form_class(request.POST)
        if not form.is_valid():
            messages.error(request, "Unable to confirm import. Please try again.")
            return redirect(
                reverse("pmksy:wizard", kwargs={"wizard_slug": self.wizard_slug})
            )

        run = self._get_user_run(form.cleaned_data["run_id"])

        try:
            result = run.run_all(run.get_auto_import_tasks())
        except InputNeeded as exc:  # pragma: no cover - defensive
            logger.warning("Import requires additional input: action=%s", exc.action)
            messages.warning(
                request,
                "Additional configuration is required before importing this dataset.",
            )
            return redirect(run.get_absolute_url())

        if isinstance(result, dict):
            if result.get("error"):
                messages.error(request, result["error"])
                return redirect(
                    f"{reverse('pmksy:wizard', kwargs={'wizard_slug': self.wizard_slug})}?run={run.pk}"
                )
            if result.get("action"):
                messages.warning(
                    request,
                    "Further setup is required via the advanced wizard interface.",
                )
                return redirect(run.get_absolute_url())

        messages.success(
            request,
            f"Successfully imported data for {self.wizard_config['name']}.",
        )
        context = {"wizard": self.wizard_config, "run": run}
        return render(request, self.success_template_name, context)

    def _get_user_run(self, run_id: int) -> Run:
        try:
            run = Run.objects.get(pk=run_id, user=self.request.user)
        except Run.DoesNotExist as exc:  # pragma: no cover - defensive
            raise Http404("Import session not found") from exc
        return run
