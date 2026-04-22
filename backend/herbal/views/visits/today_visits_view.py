from django.views.generic import ListView
from django.utils import timezone
from herbal.models.visits.visit_schedule_model import VisitSchedule

class TodayVisitsListView(ListView):
    model = VisitSchedule
    template_name = "herbal/visits/today_visits.html"
    context_object_name = "visits"
    paginate_by = 10

    def get_queryset(self):
        today = timezone.now().date()
        return VisitSchedule.objects.select_related(
            "enrollment__screening__subject", "visit_day"
        ).filter(
            scheduled_date=today,
            status="pending"
        ).order_by("enrollment__screening__subject__subject_id")

today_visits_view = TodayVisitsListView.as_view()
