from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import Enrollment
from herbal.forms.enrollment_form import EnrollmentForm
from herbal.services.visit_scheduler import generate_visit_schedule


@login_required
def enrollment_update_view(request, pk):

    enrollment = get_object_or_404(Enrollment, pk=pk)

    subject = enrollment.screening.subject

    old_enrollment_date = enrollment.enrollment_date

    if request.method == "POST":

        form = EnrollmentForm(request.POST, instance=enrollment)

        if form.is_valid():

            enrollment = form.save()

            # If enrollment date changed → update visits
            if enrollment.enrollment_date != old_enrollment_date:

                generate_visit_schedule(enrollment)

            return redirect(
                "herbal:subjects-detail",
                pk=subject.pk
            )

    else:

        form = EnrollmentForm(instance=enrollment)

    return render(
        request,
        "herbal/enrollments/enrollment_form.html",
        {
            "form": form,
            "enrollment": enrollment,
            "subject": subject,
            "is_update": True,
        }
    )