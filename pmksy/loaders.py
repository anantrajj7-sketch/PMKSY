"""Custom data-wizard loaders for PMKSY imports."""

from __future__ import annotations

from typing import Dict

from data_wizard.loaders import FileLoader as DataWizardFileLoader

from .models import ImportRunMetadata


class WorkbookAwareFileLoader(DataWizardFileLoader):
    """Attach workbook-specific metadata (e.g., sheet name) to the loader."""

    def load_iter_options(self) -> Dict[str, object]:
        options = super().load_iter_options()

        try:
            metadata = self.run.pmksy_metadata
        except ImportRunMetadata.DoesNotExist:
            metadata = None

        sheet_name = getattr(metadata, "sheet_name", "")
        if sheet_name:
            # Copy options to avoid mutating the parent's cached dictionary.
            options = dict(options)
            options["sheet_name"] = sheet_name

        return options
