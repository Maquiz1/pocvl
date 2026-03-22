from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.core.exceptions import ObjectDoesNotExist

from herbal.services.access_control import get_accessible_subjects
from herbal.models import Screening, VisitSchedule, CRF5, Enrollment
from herbal.models.queries.query_model import DataQuery
from herbal.models import UnscheduledVisit


@login_required
def subject_detail_view(request, pk):

    # ---------------- ACCESS CONTROL ----------------
    subjects = get_accessible_subjects(request.user)
    subject = get_object_or_404(subjects, pk=pk)

    # ---------------- SCREENING ----------------
    screening = (
        Screening.objects
        .filter(subject=subject)
        .first()
    )

    # ---------------- ENROLLMENT (SAFE ✅) ----------------
    enrollment = None
    if screening:
        enrollment = Enrollment.objects.filter(screening=screening).first()

    # ---------------- VISITS ----------------
    visits = []
    scheduled_visits = VisitSchedule.objects.none()
    unscheduled_visits = UnscheduledVisit.objects.none()
    
    if enrollment:
        scheduled_visits = (
            VisitSchedule.objects
            .filter(enrollment=enrollment)
            .order_by("scheduled_date")
        )

        unscheduled_visits = (
            enrollment.unscheduled_visits
            .select_related("after_visit")
            .all()
        )

        visits = list(scheduled_visits)
        # # 🔥 MAP unscheduled → parent visit
        # unscheduled_map = {}
        # for u in unscheduled_visits:
        #     unscheduled_map.setdefault(u.after_visit_id, []).append(u)

        # # 🔥 MERGE visits
        # for visit in scheduled_visits:
        #     visits.append(visit)
        #     visits.extend(unscheduled_map.get(visit.id, []))

    # ---------------- ADVERSE EVENTS ----------------
    adverse_events = CRF5.objects.none()

    if enrollment:
        adverse_events = (
            CRF5.objects
            .filter(enrollment=enrollment)
            .order_by("-event_date")
        )

    # ---------------- LTFU ----------------
    is_ltfu = False
    if enrollment:
        termination = getattr(enrollment, "termination", None)
        if termination:
            is_ltfu = termination.reason == "ltf"


    # ---------------- VISIT STATS ----------------
    visit_stats = scheduled_visits.aggregate(
        total=Count("id"),
        completed=Count("id", filter=Q(status="completed"))
    )

    total_visits = visit_stats["total"] or 0
    completed_visits = visit_stats["completed"] or 0

    progress_percent = int((completed_visits / total_visits) * 100) if total_visits > 0 else 0

    # ---------------- QUERIES ----------------
    queries = DataQuery.objects.filter(visit__in=scheduled_visits)

    # ---------------- CONTEXT ----------------
    context = {
        "subject": subject,
        "screening": screening,
        "enrollment": enrollment,
        "visits": visits,
        "adverse_events": adverse_events,
        "unscheduled_visits": unscheduled_visits,
        "is_ltfu": is_ltfu,

        "completed_visits": completed_visits,
        "total_visits": total_visits,
        "progress_percent": progress_percent,

        "queries": queries,
    }

    return render(
        request,
        "herbal/subjects/subject_detail.html",
        context
    )