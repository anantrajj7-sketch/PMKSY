from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .views import PREVIEW_ERROR_MESSAGE


class PMKSYImportWizardPreviewTests(TestCase):
    """Tests for PMKSY import wizard preview handling."""

    def setUp(self) -> None:
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="password123",
        )
        self.client.force_login(self.user)
        self.wizard_url = reverse("pmksy:wizard", kwargs={"wizard_slug": "farmers"})

    def test_invalid_workbook_redirects_with_message(self) -> None:
        """An invalid workbook should surface a helpful error message."""

        class BrokenLoader:
            def __init__(self, run):  # pragma: no cover - simple data holder
                self.run = run

            def load_iter(self):
                raise ValueError("Unsupported workbook format")

        uploaded_file = SimpleUploadedFile(
            "invalid.xlsx",
            b"not a real workbook",
            content_type=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        )

        with mock.patch(
            "pmksy.views.data_wizard_registry.get_loader", return_value=BrokenLoader
        ):
            with self.assertLogs("pmksy.views", level="ERROR") as logs:
                response = self.client.post(
                    self.wizard_url, {"source_file": uploaded_file}, follow=True
                )

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[-1][0], self.wizard_url)

        messages = [message.message for message in response.context["messages"]]
        self.assertIn(PREVIEW_ERROR_MESSAGE, messages)

        self.assertTrue(
            any("Failed to generate preview" in message for message in logs.output)
        )
