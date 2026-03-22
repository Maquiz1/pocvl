from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import Subject
from herbal.forms.enrollment_form import EnrollmentForm
from herbal.services.visit_scheduler import generate_visit_schedule
from herbal.services.access_control import get_accessible_subjects


@login_required
def enrollment_create_view(request, pk):

    subjects = get_accessible_subjects(request.user)

    subject = get_object_or_404(subjects, pk=pk)

    screening = getattr(subject, "screening", None)

    # must have screening
    if not screening:
        return redirect("herbal:subjects-detail", pk=subject.pk)

    # must be eligible
    if not screening.eligible:
        return redirect("herbal:subjects-detail", pk=subject.pk)

    # prevent duplicate enrollment
    if hasattr(screening, "enrollment"):
        return redirect("herbal:subjects-detail", pk=subject.pk)

    if request.method == "POST":

        form = EnrollmentForm(request.POST)

        if form.is_valid():

            enrollment = form.save(commit=False)

            enrollment.screening = screening

            enrollment.save()

            # generate visit schedule
            generate_visit_schedule(enrollment)

            return redirect(
                "herbal:subjects-detail",
                pk=subject.pk
            )

    else:

        form = EnrollmentForm()

    context = {
        "form": form,
        "subject": subject,
        "screening": screening
    }

    return render(
        request,
        "herbal/enrollments/enrollment_form.html",
        context
    )