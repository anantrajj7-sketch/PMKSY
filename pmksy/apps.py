from django.apps import AppConfig


class PmksyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pmksy"

    def ready(self) -> None:  # pragma: no cover - import side effects only
        from . import importers  # noqa: F401

        return super().ready()
