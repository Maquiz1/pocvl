from django.urls import path
from . import views

urlpatterns = [
    path('export-data/', views.export_models_view, name='export_models'),
]