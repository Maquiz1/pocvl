from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

def root_redirect(request):

    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")

    return redirect("accounts:login")


urlpatterns = [

    path("admin/", admin.site.urls),

    # root redirect
    path("", root_redirect),

    # herbal app (dashboard namespace)
    path("", include(("dashboard.urls"), namespace="dashboard")),

    # accounts app
    path("accounts/", include("accounts.urls")),
    
    path("herbal/", include("herbal.urls")),
    
    
    path("locations/", include("locations.urls")),
    
    path("exports/", include("exports.urls")),
    
    path("utils/",include("utils.urls")),

    path("reports/", include("reports.urls", namespace="reports")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
