from django.urls import path
from .views import (
    EmailRecipientListView,
    EmailRecipientCreateView,
    EmailRecipientUpdateView,
    EmailRecipientDeleteView,
    
    SiteConfigurationListView,
    SiteConfigurationCreateView,
    SiteConfigurationUpdateView, 
    SiteConfigurationDeleteView,
)

app_name = 'utils'

urlpatterns = [
    path("recipients/", EmailRecipientListView.as_view(), name="email_recipient_list"),
    path("recipients/add/", EmailRecipientCreateView.as_view(), name="email_recipient_add"),
    path("recipients/<int:pk>/edit/", EmailRecipientUpdateView.as_view(), name="email_recipient_edit"),
    path("recipients/<int:pk>/delete/", EmailRecipientDeleteView.as_view(), name="email_recipient_delete"),
    
    path("site-config/", SiteConfigurationListView.as_view(), name="site_configuration_list"),
    path("site-config/add/", SiteConfigurationCreateView.as_view(), name="site_config_add"),
    path("site-config/<int:pk>/edit/", SiteConfigurationUpdateView.as_view(), name="site_config_edit"),
    path("site-config/<int:pk>/delete/", SiteConfigurationDeleteView.as_view(), name="site_config_delete"), 
]

