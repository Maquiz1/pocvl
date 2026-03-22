from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from herbal.models import Enrollment, VisitSchedule
from herbal.forms.crfs.crf6_form import CRF6Form


@login_required
def crf6_create_view(request, pk):

    enrollment = get_object_or_404(Enrollment, pk=pk)

    subject = enrollment.screening.subject

    if hasattr(enrollment, "termination"):
        return redirect("herbal:subjects-detail", pk=subject.pk)

    if request.method == "POST":

        form = CRF6Form(request.POST)

        if form.is_valid():

            crf = form.save(commit=False)

            crf.enrollment = enrollment

            crf.save()

            # mark enrollment terminated
            enrollment.status = "terminated"
            enrollment.save()

            # Reset visits before new termination date
            VisitSchedule.objects.filter(
                enrollment=enrollment,
                scheduled_date__lte=crf.termination_date,
                status="na"
            ).update(status="pending")

            # Set future visits to NA
            VisitSchedule.objects.filter(
                enrollment=enrollment,
                scheduled_date__gt=crf.termination_date,
                status="pending"
            ).update(status="na")

            return redirect(
                "herbal:subjects-detail",
                pk=subject.pk
            )

    else:

        form = CRF6Form()

    return render(
        request,
        "herbal/crfs/crf6/crf6_form.html",
        {
            "form": form,
            "enrollment": enrollment,
            "subject": subject,
        }
    )