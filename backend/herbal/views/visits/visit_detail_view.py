from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models.visits.visit_schedule_model import VisitSchedule


@login_required
def visit_detail_view(request, pk):
    visit = get_object_or_404(
        VisitSchedule.objects.select_related(
            "enrollment__screening__subject",
            "visit_day"
        ),
        pk=pk,
    )

    return render(request, "herbal/visits/visit_detail.html", {
        "visit": visit,
        "today": timezone.now().date(),
    })