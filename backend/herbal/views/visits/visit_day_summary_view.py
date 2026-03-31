from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Q
from herbal.models.visits.visit_schedule_model import VisitSchedule


@login_required
def visit_day_summary_view(request):

    from django.db.models import Count, Q

    visits = (
    VisitSchedule.objects
    .select_related("visit_day", "enrollment")
    .values("visit_day__id", "visit_day__code", "visit_day__name")
    .annotate(
        total_visits=Count("id"),

        # Direct CRFs
        crf1=Count("crf1", filter=Q(crf1__isnull=False)),
        crf2=Count("crf2", filter=Q(crf2__isnull=False)),
        crf3=Count("crf3", filter=Q(crf3__isnull=False)),
        crf4=Count("crf4", filter=Q(crf4__isnull=False)),
        crf7=Count("crf7", filter=Q(crf7__isnull=False)),

        # Indirect CRFs (via enrollment)
        # crf5=Count("enrollment__crf5", filter=Q(enrollment__crf5__isnull=False)),
        # crf6=Count("enrollment__crf6", filter=Q(enrollment__crf6__isnull=False)),
    )
    .order_by("visit_day__id")
)

    context = {
        "summary": visits
    }

    return render(
        request,
        "herbal/visits/visit_day_summary.html",
        context
    )