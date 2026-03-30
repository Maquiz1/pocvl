from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from herbal.models.visits.visit_schedule_model import VisitSchedule


@login_required
def visit_day_summary_view(request):

    visits = VisitSchedule.objects.select_related("visit_day")

    summary = {}

    for visit in visits:

        day = visit.visit_day.code  # or name

        if day not in summary:
            summary[day] = {
                "visit_day": visit.visit_day,
                "crf1": 0,
                "crf2": 0,
                "crf3": 0,
                "crf4": 0,
                "crf5": 0,
                "crf6": 0,
                "crf7": 0,
                "total_visits": 0,
            }

        summary[day]["total_visits"] += 1

        if hasattr(visit, "crf1"):
            summary[day]["crf1"] += 1
        if hasattr(visit, "crf2"):
            summary[day]["crf2"] += 1
        if hasattr(visit, "crf3"):
            summary[day]["crf3"] += 1
        if hasattr(visit, "crf4"):
            summary[day]["crf4"] += 1
        if hasattr(visit, "crf5"):
            summary[day]["crf5"] += 1
        if hasattr(visit, "crf6"):
            summary[day]["crf6"] += 1
        if hasattr(visit, "crf7"):
            summary[day]["crf7"] += 1

    context = {
        "summary": summary.values()
    }

    return render(
        request,
        "herbal/visits/visit_day_summary.html",
        context
    )