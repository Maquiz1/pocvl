from django.views.generic import ListView
from django.utils import timezone
from herbal.models.visits.visit_schedule_model import VisitSchedule

class VisitAfterListView(ListView):
    model = VisitSchedule
    template_name = "herbal/visits/visit_after.html"
    context_object_name = "visits"
    paginate_by = 10

    def get_queryset(self):
        today = timezone.now().date()
        return VisitSchedule.objects.select_related(
            "enrollment", "visit_day", "subject"
        ).filter(
            scheduled_date__gt=today,
            status="pending"
        ).order_by("scheduled_date")

visit_after_view = VisitAfterListView.as_view()
