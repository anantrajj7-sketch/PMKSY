from django.apps import AppConfig


class PmksyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pmksy"

    def ready(self) -> None:  # pragma: no cover - import side effects only
        from data_wizard.views import RunViewSet

        from . import importers  # noqa: F401
        from .serializers import ImportRecordSerializer

        RunViewSet.record_serializer_class = ImportRecordSerializer

        return super().ready()
