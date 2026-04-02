from django.urls import path
from . import views

app_name = "exports"

urlpatterns = [
    path("export/", views.export_page, name="export_page"),
    path("export/start/", views.start_export, name="start_export"),
    path("export/status/<str:task_id>/", views.export_status, name="export_status"),
    path("export/download/", views.download_export, name="download_export"),
    path("export-data/", views.export_models_view, name="export_models"),
    path("export-list/", views.export_list_view, name="export_list"),
]
