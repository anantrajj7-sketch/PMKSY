from __future__ import annotations

import tempfile
from urllib.parse import parse_qs, urlparse

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from data_wizard.models import Identifier, Run

from ..models import Farmer


class FarmersImportUUIDTests(TestCase):
    """Regression tests for importing Farmers data with UUID primary keys."""

    def setUp(self) -> None:
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="uuidtester",
            email="uuidtester@example.com",
            password="password123",
        )
        self.client.force_login(self.user)
        self.wizard_url = reverse("pmksy:wizard", kwargs={"wizard_slug": "farmers"})

    def test_import_handles_uuid_primary_keys(self) -> None:
        """The import task should not overflow when models use UUID PKs."""

        Identifier.objects.create(
            serializer="Farmers",
            name="name",
            field="name",
            resolved=True,
        )

        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            upload = SimpleUploadedFile(
                "farmers.csv",
                "name\nTest Farmer\n".encode("utf-8"),
                content_type="text/csv",
            )
            response = self.client.post(self.wizard_url, {"source_file": upload})

            self.assertEqual(response.status_code, 302)
            redirect_url = response["Location"]
            run_id = parse_qs(urlparse(redirect_url).query)["run"][0]

            preview_response = self.client.get(redirect_url)
            self.assertEqual(preview_response.status_code, 200)
            self.assertIn("Test Farmer", preview_response.content.decode())

            confirm_response = self.client.post(
                self.wizard_url, {"run_id": run_id}, follow=True
            )

        self.assertEqual(confirm_response.status_code, 200)
        self.assertIn("Import Complete", confirm_response.content.decode())

        self.assertEqual(Farmer.objects.count(), 1)
        run = Run.objects.get(pk=int(run_id))
        record = run.record_set.get()
        self.assertTrue(record.success)
        self.assertIsNone(record.object_id)
        self.assertIsNotNone(record.content_type)
        self.assertEqual(record.content_type.model, "farmer")
        self.assertEqual(run.record_count, 1)
