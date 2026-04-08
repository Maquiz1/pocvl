from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from accounts.views import (
    CustomLoginView, 
    force_logout, 
    CustomPasswordResetView,
    StaffListView,
    StaffCreateUpdateView,
    resend_credentials_view
)

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", force_logout, name="logout"),
    
    # User Management
    path('staff/', StaffListView.as_view(), name='staff_list'),
    path('staff/create/', StaffCreateUpdateView.as_view(), name='staff_create'),
    path('staff/<int:pk>/update/', StaffCreateUpdateView.as_view(), name='staff_update'),
    path('staff/<int:pk>/resend-credentials/', resend_credentials_view, name='resend_credentials'),

    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),

    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),

    path(
        "session-expired/",
        TemplateView.as_view(
            template_name="registration/session_expired.html"
        ),
        name="session_expired",
    ),
]