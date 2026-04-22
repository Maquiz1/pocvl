from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta

from herbal.models.visits.visit_schedule_model import VisitSchedule


def visit_dashboard_view(request):

    today = timezone.now().date()
    one_day_before_date = today - timedelta(days=1)
    three_days_before_date = today - timedelta(days=3)
    one_day_after_date = today + timedelta(days=1)
    three_days_after_date = today + timedelta(days=3)

    visits = VisitSchedule.objects.select_related(
        "enrollment__screening__subject",
        "visit_day"
    )

    due_today = visits.filter(
        scheduled_date=today,
        status="pending"
    )

    one_day_before = visits.filter(
        scheduled_date=one_day_before_date,
        status="pending"
    )

    three_days_before = visits.filter(
        scheduled_date=three_days_before_date,
        status="pending"
    )

    one_day_after = visits.filter(
        scheduled_date=one_day_after_date,
        status="pending"
    )

    three_days_after = visits.filter(
        scheduled_date=three_days_after_date,
        status="pending"
    )

    overdue = visits.filter(
        scheduled_date__lt=today,
        status="pending"
    )

    upcoming = visits.filter(
        scheduled_date__gt=today,
        status="pending"
    )

    completed = visits.filter(
        status="completed"
    )

    def paginate(queryset, page_param, per_page=10):
        paginator = Paginator(queryset, per_page)
        page_number = request.GET.get(page_param, 1)
        return paginator.get_page(page_number)

    overdue_page = paginate(overdue, "overdue_page")
    due_today_page = paginate(due_today, "due_today_page")
    one_day_before_page = paginate(one_day_before, "one_day_before_page")
    three_days_before_page = paginate(three_days_before, "three_days_before_page")
    one_day_after_page = paginate(one_day_after, "one_day_after_page")
    three_days_after_page = paginate(three_days_after, "three_days_after_page")
    upcoming_page = paginate(upcoming, "upcoming_page")
    completed_page = paginate(completed, "completed_page")

    context = {
        "due_today": due_today_page,
        "one_day_before": one_day_before_page,
        "three_days_before": three_days_before_page,
        "one_day_after": one_day_after_page,
        "three_days_after": three_days_after_page,
        "overdue": overdue_page,
        "upcoming": upcoming_page,
        "completed": completed_page,

        "due_today_count": due_today.count(),
        "one_day_before_count": one_day_before.count(),
        "three_days_before_count": three_days_before.count(),
        "one_day_after_count": one_day_after.count(),
        "three_days_after_count": three_days_after.count(),
        "overdue_count": overdue.count(),
        "upcoming_count": upcoming.count(),
        "completed_count": completed.count(),
    }

    return render(
        request,
        "herbal/visits/visit_dashboard.html",
        context
    )
