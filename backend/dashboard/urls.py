from django.urls import path
from .views.dashboard import dashboard_view,monitor_dashboard_view


app_name = "dashboard"

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("monitor_dashboard_view/", monitor_dashboard_view, name="monitor_dashboard_view"),
]
