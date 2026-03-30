from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from herbal.models.visits.visit_schedule_model import VisitSchedule


@login_required
def visit_registry_view(request):

    visits = VisitSchedule.objects.select_related(
        "enrollment__screening__subject",
        "visit_day"
    ).prefetch_related(
        "crf1",
        "crf2",
        "crf3",
        "crf4",
        # "crf5",
        # "crf6",
        "crf7",
    ).order_by("enrollment__screening__subject")

    visit_data = []

    for visit in visits:

        crf_status = {
            "crf1": hasattr(visit, "crf1"),
            "crf2": hasattr(visit, "crf2"),
            "crf3": hasattr(visit, "crf3"),
            "crf4": hasattr(visit, "crf4"),
            "crf5": hasattr(visit, "crf5"),
            "crf6": hasattr(visit, "crf6"),
            "crf7": hasattr(visit, "crf7"),
        }

        completed = sum(crf_status.values())

        visit_data.append({
            "visit": visit,
            "crfs": crf_status,
            "completed": completed,
            "total": 7,
        })

    return render(
        request,
        "herbal/visits/visit_registry.html",
        {"visits": visit_data}
    )