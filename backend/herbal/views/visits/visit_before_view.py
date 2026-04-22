from django.views.generic import ListView
from django.utils import timezone
from herbal.models.visits.visit_schedule_model import VisitSchedule

class VisitBeforeListView(ListView):
    model = VisitSchedule
    template_name = "herbal/visits/visit_before.html"
    context_object_name = "visits"
    paginate_by = 10

    def get_queryset(self):
        today = timezone.now().date()
        return VisitSchedule.objects.select_related(
            "enrollment__screening__subject", "visit_day"
        ).filter(
            scheduled_date__lt=today,
            status="pending"
        ).order_by("-scheduled_date")

visit_before_view = VisitBeforeListView.as_view()
