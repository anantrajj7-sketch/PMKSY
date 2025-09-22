"""Custom data import tasks for PMKSY."""

from __future__ import annotations

import uuid
from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db import models

from data_wizard.tasks import (
    get_rows,
    import_complete,
    import_row,
    reversion,
    wizard_task,
)


@wizard_task(label="Importing Data...", url_path="data", use_async=True)
def import_data(run):
    """Import all parseable data from the dataset instance's Iter class."""
    if reversion:
        with reversion.create_revision():
            reversion.set_user(run.user)
            reversion.set_comment("Imported via %s" % run)
            result = _do_import(run)
    else:
        result = _do_import(run)
    return result


def _do_import(run):
    run.add_event("do_import")

    # Loop through table rows and add each record
    table = run.load_iter()
    rows = len(table)
    skipped: list[dict[str, Any]] = []

    if table.tabular:

        def rownum(i):
            return i + table.start_row

    else:

        def rownum(i):
            return i

    for i, row in enumerate(get_rows(run)):
        # Update state (for status() on view)
        run.send_progress(
            {
                "message": "Importing Data...",
                "stage": "data",
                "current": i,
                "total": rows,
                "skipped": skipped,
            }
        )

        # Create report, capturing any errors
        obj, error = import_row(run, i, row)
        if error:
            success = False
            fail_reason = error
            skipped.append({"row": rownum(i) + 1, "reason": fail_reason})
        else:
            success = True
            fail_reason = None

        # Record relationship between data source and resulting report (or
        # skipped record), including specific cell range.
        record = run.record_set.model(
            run=run,
            row=rownum(i),
            success=success,
            fail_reason=fail_reason,
        )
        _set_record_object(record, obj)
        record.save()

    # Send completion signal (in case any server handlers are registered)
    status = {"current": i + 1, "total": rows, "skipped": skipped}
    run.add_event("import_complete")
    run.record_count = run.record_set.filter(success=True).count()
    run.save()
    run.send_progress(status, state="SUCCESS")
    import_complete.send(sender=import_data, run=run, status=status)

    return status


def _set_record_object(record, obj: Any) -> None:
    """Attach ``obj`` to ``record`` while gracefully handling UUID keys."""

    if not isinstance(obj, models.Model):
        return

    if _has_uuid_primary_key(obj):
        record.content_type = ContentType.objects.get_for_model(
            obj, for_concrete_model=False
        )
        record.object_id = None
    else:
        record.content_object = obj


def _has_uuid_primary_key(obj: models.Model) -> bool:
    """Return ``True`` if ``obj`` is backed by a UUID primary key."""

    pk_field = obj._meta.pk
    if isinstance(pk_field, models.UUIDField):
        return True

    pk_value = getattr(obj, pk_field.attname, None)
    if isinstance(pk_value, uuid.UUID):
        return True

    if isinstance(pk_value, str):
        try:
            uuid.UUID(pk_value)
        except (TypeError, ValueError, AttributeError):
            return False
        else:
            return True

    return False
