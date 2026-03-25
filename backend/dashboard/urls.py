from django.urls import path
from .views.dashboard import dashboard_view,monitor_dashboard_view,visit_dashboard_view


app_name = "dashboard"

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("monitor_dashboard_view/", monitor_dashboard_view, name="monitor_dashboard_view"),
    path("dashboard/visit-dashboard/", visit_dashboard_view, name="visit-dashboard"),
]
