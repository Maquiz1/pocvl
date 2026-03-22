from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count

from herbal.models import Subject, Enrollment, VisitSchedule
from herbal.models.crfs.crf5.crf5_model import CRF5
from sites.models import Site


@login_required
def monitor_dashboard_view(request):

    user = request.user
    profile = user.staff_profile
    role = profile.role

    subjects = Subject.objects.all()

    # ROLE FILTERING
    if role in ["data_clerk", "coordinator"]:
        subjects = subjects.filter(site=profile.site)

    elif role in ["monitor", "reviewer", "pi"]:
        subjects = subjects.filter(site__in=profile.assigned_sites.all())

    today = timezone.now().date()

    enrollments = Enrollment.objects.filter(
        screening__subject__in=subjects
    )

    visits = VisitSchedule.objects.filter(
        enrollment__in=enrollments
    )

    # OVERDUE VISITS
    overdue_visits = visits.filter(
        status="pending",
        scheduled_date__lt=today
    )

    # MISSED VISITS
    missed_visits = visits.filter(status="missed")

    # ADVERSE EVENTS
    adverse_events = CRF5.objects.filter(
        enrollment__in=enrollments
    )

    # SITE PERFORMANCE
    site_summary = (
        Site.objects
        .filter(subject__in=subjects)
        .annotate(total_subjects=Count("subject"))
        .order_by("-total_subjects")
    )

    # SUBJECT STATUS
    active_subjects = enrollments.filter(status="active").count()

    terminated_subjects = enrollments.filter(status="terminated").count()

    lost_subjects = enrollments.filter(status="lost").count()

    context = {

        "overdue_visits": overdue_visits,
        "missed_visits": missed_visits,
        "adverse_events": adverse_events,

        "site_summary": site_summary,

        "active_subjects": active_subjects,
        "terminated_subjects": terminated_subjects,
        "lost_subjects": lost_subjects,
    }

    return render(
        request,
        "dashboard/monitor_dashboard.html",
        context
    )