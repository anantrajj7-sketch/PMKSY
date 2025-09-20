"""URL configuration for the PMKSY app."""

from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "pmksy"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="pmksy:import-home", permanent=False)),
    path("import/", views.ImportHomeView.as_view(), name="import-home"),
    path(
        "import/<slug:wizard_slug>/",
        views.PMKSYImportWizard.as_view(),
        name="wizard",
    ),
]
