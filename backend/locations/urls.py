# locations/urls.py
from django.urls import path
from . import views


app_name="locations"

urlpatterns = [
    path("regions/", views.search_regions, name="search_regions"),
    path("districts/", views.search_districts, name="search_districts"),
    path("wards/", views.search_wards, name="search_wards"),
]