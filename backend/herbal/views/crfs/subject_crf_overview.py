from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import Subject


@login_required
def subject_crf_overview(request, pk):

    subject = get_object_or_404(
        Subject.objects.select_related(
            "screening",
            "screening__enrollment"
        ).prefetch_related(
            "screening__enrollment__visits__crf1",
            "screening__enrollment__visits__crf2",
            "screening__enrollment__visits__crf3",
            "screening__enrollment__visits__crf4",
            "screening__enrollment__visits__crf7",
        ),
        pk=pk
    )

    enrollment = getattr(subject.screening, "enrollment", None)

    visits = []
    if enrollment:
        visits = enrollment.visits.all().order_by("scheduled_date")

    context = {
        "subject": subject,
        "visits": visits,
    }

    return render(
        request,
        "herbal/crfs/crf_overview.html",
        context
    )