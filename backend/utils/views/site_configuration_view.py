from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import SiteConfiguration

class SiteConfigurationListView(ListView):
    model = SiteConfiguration
    template_name = "utils/site_config/list.html"
    context_object_name = "configs"

    def get_queryset(self):
        return SiteConfiguration.objects.filter(is_deleted=False)


class SiteConfigurationCreateView(CreateView):
    model = SiteConfiguration
    fields = ["name", "site_url", "is_active"]
    template_name = "utils/site_config/add.html"
    success_url = reverse_lazy("utils:site_configuration_list")


class SiteConfigurationUpdateView(UpdateView):
    model = SiteConfiguration
    fields = ["name", "site_url", "is_active"]
    template_name = "utils/site_config/edit.html"
    success_url = reverse_lazy("utils:site_configuration_list")


class SiteConfigurationDeleteView(DeleteView):
    model = SiteConfiguration
    template_name = "utils/site_config/delete.html"
    success_url = reverse_lazy("utils:site_configuration_list")

    def delete(self, request, *args, **kwargs):
        """Soft delete instead of removing from DB."""
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.is_active = False
        self.object.save(update_fields=["is_deleted", "is_active"])
        return super().delete(request, *args, **kwargs)
