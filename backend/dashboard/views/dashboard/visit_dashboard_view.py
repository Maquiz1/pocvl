from django.shortcuts import render
from django.db.models import Count, Q
from django.utils import timezone
from django.db.models.functions import TruncMonth
from collections import defaultdict
import json

from herbal.models import Subject


def visit_dashboard_view(request):

    queryset = Subject.objects.for_user(request.user)

    # ---------------- VISIT STATS ----------------
    stats = queryset.aggregate(

        total_visits=Count("screening__enrollment__visits", distinct=True),

        attended_visits=Count(
            "screening__enrollment__visits",
            filter=Q(screening__enrollment__visits__status__in=["completed", "incomplete"]),
            distinct=True
        ),

        completed_visits=Count(
            "screening__enrollment__visits",
            filter=Q(screening__enrollment__visits__status="completed"),
            distinct=True
        ),

        missed_visits=Count(
            "screening__enrollment__visits",
            filter=Q(screening__enrollment__visits__status="missed"),
            distinct=True
        ),

        pending_visits=Count(
            "screening__enrollment__visits",
            filter=Q(screening__enrollment__visits__status="pending"),
            distinct=True
        ),

        overdue_visits=Count(
            "screening__enrollment__visits",
            filter=Q(
                screening__enrollment__visits__status="pending",
                screening__enrollment__visits__scheduled_date__lt=timezone.now().date()
            ),
            distinct=True
        ),
    )

    total = stats["total_visits"] or 0
    attended = stats["attended_visits"] or 0
    attendance_rate = int((attended / total) * 100) if total else 0

    # ---------------- SITE COMPARISON ----------------
    site_stats = (
        queryset
        .values("site__name")
        .annotate(
            total=Count("screening__enrollment__visits", distinct=True),

            attended=Count(
                "screening__enrollment__visits",
                filter=Q(screening__enrollment__visits__status__in=["completed", "incomplete"]),
                distinct=True
            ),

            completed=Count(
                "screening__enrollment__visits",
                filter=Q(screening__enrollment__visits__status="completed"),
                distinct=True
            ),

            missed=Count(
                "screening__enrollment__visits",
                filter=Q(screening__enrollment__visits__status="missed"),
                distinct=True
            ),

            pending=Count(
                "screening__enrollment__visits",
                filter=Q(screening__enrollment__visits__status="pending"),
                distinct=True
            ),
        )
    )

    # ---------------- MONTHLY TRENDS ----------------
    monthly_stats = (
        queryset
        .annotate(month=TruncMonth("screening__enrollment__visits__scheduled_date"))
        .values("month", "site__name")
        .annotate(
            total=Count("screening__enrollment__visits", distinct=True)
        )
        .order_by("month")
    )

    # Transform for chart
    trend_data = defaultdict(lambda: {"months": [], "data": []})

    for row in monthly_stats:
        site = row["site__name"]
        month = row["month"].strftime("%b %Y") if row["month"] else "N/A"

        trend_data[site]["months"].append(month)
        trend_data[site]["data"].append(row["total"])

    # Extract labels (IMPORTANT FIX)
    labels = []
    if trend_data:
        first_site = next(iter(trend_data.values()))
        labels = first_site["months"]

    # ---------------- KPI DASHBOARD ----------------
    kpis = queryset.aggregate(

        total_subjects=Count("id", distinct=True),

        enrolled=Count(
            "id",
            filter=Q(screening__enrollment__isnull=False),
            distinct=True
        ),

        completed_visits=Count(
            "screening__enrollment__visits",
            filter=Q(screening__enrollment__visits__status="completed"),
            distinct=True
        ),

        missed_visits=Count(
            "screening__enrollment__visits",
            filter=Q(screening__enrollment__visits__status="missed"),
            distinct=True
        ),
    )

    enrollment_rate = int(
        (kpis["enrolled"] / kpis["total_subjects"]) * 100
    ) if kpis["total_subjects"] else 0

    completion_rate = int(
        (kpis["completed_visits"] / stats["total_visits"]) * 100
    ) if stats["total_visits"] else 0

    kpis.update({
        "enrollment_rate": enrollment_rate,
        "completion_rate": completion_rate,
    })

    # ---------------- FINAL CONTEXT ----------------
    context = {
        **stats,
        "attendance_rate": attendance_rate,
        "site_stats": site_stats,
        "kpis": kpis,

        # 🔥 FIXED FOR TEMPLATE
        "trend_labels": json.dumps(labels),
        "trend_data": json.dumps(trend_data),
    }

    return render(
        request,
        "dashboard/visit_dashboard.html",
        context
    )