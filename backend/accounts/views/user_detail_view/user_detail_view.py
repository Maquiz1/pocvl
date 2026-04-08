from django.views.generic import DetailView
from django.contrib.auth import get_user_model

User = get_user_model()

class StaffDetailView(DetailView):
    model = User
    template_name = "users/staff/staff_detail.html"
    context_object_name = "staff"

    def get_queryset(self):
        return super().get_queryset().select_related(
            "staff_profile",
            "staff_profile__prefix",
            "staff_profile__position",
            "staff_profile__site",
        ).prefetch_related("groups")
