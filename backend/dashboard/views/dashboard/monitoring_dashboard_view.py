from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone

from herbal.models.visits.visit_schedule_model import VisitSchedule


@login_required
def monitoring_view(request):

    today = timezone.now().date()

    visits = VisitSchedule.objects.select_related(
        "enrollment__screening__subject",
        "visit_day"
    ).prefetch_related(
        "crf1",
        "crf2",
        "crf3",
        "crf4",
        "crf7",
    )

    monitoring_data = []

    for visit in visits:

        # =========================
        # CRF STATUS
        # =========================
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
        total = 7

        # =========================
        # STATUS FLAGS
        # =========================
        is_overdue = (
            visit.status == "pending" and visit.scheduled_date < today
        )

        is_today = visit.scheduled_date == today

        is_upcoming = visit.scheduled_date > today

        # Missing CRFs (important for monitoring)
        missing_crfs = [k for k, v in crf_status.items() if not v]

        monitoring_data.append({
            "visit": visit,
            "crfs": crf_status,
            "completed": completed,
            "total": total,
            "percent": int((completed / total) * 100),

            "is_overdue": is_overdue,
            "is_today": is_today,
            "is_upcoming": is_upcoming,

            "missing_crfs": missing_crfs,
        })

    # =========================
    # SUMMARY COUNTS
    # =========================
    total_visits = len(monitoring_data)

    overdue_count = sum(1 for v in monitoring_data if v["is_overdue"])
    today_count = sum(1 for v in monitoring_data if v["is_today"])
    upcoming_count = sum(1 for v in monitoring_data if v["is_upcoming"])

    incomplete_count = sum(1 for v in monitoring_data if v["percent"] < 100)

    paginator = Paginator(monitoring_data, 10)
    page_number = request.GET.get("page", 1)
    paginated_visits = paginator.get_page(page_number)

    # =========================
    # RESPONSE
    # =========================
    return render(request, "dashboard/monitoring_dashboard.html", {
        "visits": paginated_visits,

        # KPIs
        "total_visits": total_visits,
        "overdue_count": overdue_count,
        "today_count": today_count,
        "upcoming_count": upcoming_count,
        "incomplete_count": incomplete_count,
    })