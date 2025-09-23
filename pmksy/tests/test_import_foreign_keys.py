from __future__ import annotations

import json
import tempfile
from urllib.parse import parse_qs, urlparse

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from data_wizard.models import Run

from ..models import Farmer, LandHolding


class ForeignKeyImportTests(TestCase):
    """Ensure related datasets accept farmer names during import."""

    def setUp(self) -> None:
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="relationtester",
            email="relationtester@example.com",
            password="password123",
        )
        self.user.is_staff = True
        self.user.save(update_fields=["is_staff"])
        self.client.force_login(self.user)

        self.farmer = Farmer.objects.create(name="Jane Doe")

        self.wizard_url = reverse(
            "pmksy:wizard", kwargs={"wizard_slug": "land-holdings"}
        )

    def test_import_resolves_farmer_name_to_uuid(self) -> None:
        """Uploading a dataset with farmer names should link to the correct farmer."""

        csv_content = """farmer,category,total_area_ha
Jane Doe,Small,1.5
"""
        upload = SimpleUploadedFile(
            "land_holdings.csv",
            csv_content.encode("utf-8"),
            content_type="text/csv",
        )

        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            response = self.client.post(self.wizard_url, {"source_file": upload})

            self.assertEqual(response.status_code, 302)
            redirect_url = response["Location"]
            run_id = parse_qs(urlparse(redirect_url).query)["run"][0]

            preview_response = self.client.get(redirect_url)
            self.assertEqual(preview_response.status_code, 200)
            self.assertIn("Jane Doe", preview_response.content.decode())

            confirm_response = self.client.post(
                self.wizard_url, {"run_id": run_id}, follow=True
            )

        self.assertEqual(confirm_response.status_code, 200)
        self.assertIn("Import Complete", confirm_response.content.decode())

        land_holding = LandHolding.objects.get()
        self.assertEqual(land_holding.farmer_id, self.farmer.farmer_id)
        self.assertEqual(land_holding.category, "Small")

        run_pk = int(run_id)
        run = Run.objects.get(pk=run_pk)
        record = run.record_set.get()
        self.assertTrue(record.success)
        self.assertEqual(record.content_type.model, "landholding")
        self.assertIn(record.object_id, {None, str(land_holding.land_id)})

        records_response = self.client.get(
            reverse("data_wizard:run-records", kwargs={"pk": run_pk})
        )
        self.assertEqual(records_response.status_code, 200)
        self.assertContains(records_response, "Small")
        self.assertNotContains(records_response, ">None<")

    def test_import_without_farmer_column_reports_error(self) -> None:
        """Omitting the farmer column should surface a helpful validation error."""

        csv_content = """category,total_area_ha
Small,1.5
"""
        upload = SimpleUploadedFile(
            "land_holdings_missing_farmer.csv",
            csv_content.encode("utf-8"),
            content_type="text/csv",
        )

        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            response = self.client.post(self.wizard_url, {"source_file": upload})

            self.assertEqual(response.status_code, 302)
            redirect_url = response["Location"]
            run_id = parse_qs(urlparse(redirect_url).query)["run"][0]

            confirm_response = self.client.post(
                self.wizard_url, {"run_id": run_id}, follow=True
            )

        self.assertEqual(confirm_response.status_code, 200)
        self.assertIn("Import Complete", confirm_response.content.decode())

        run = Run.objects.get(pk=int(run_id))
        record = run.record_set.get()
        self.assertFalse(record.success)
        self.assertIsNotNone(record.fail_reason)

        error_detail = json.loads(record.fail_reason)
        self.assertEqual(
            error_detail,
            {"farmer": ["Please provide a farmer name."]},
        )
