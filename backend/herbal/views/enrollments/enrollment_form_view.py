from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import Subject, Enrollment
from herbal.forms.enrollment_form import EnrollmentForm
from herbal.services.visit_scheduler import generate_visit_schedule
from herbal.services.access_control import get_accessible_subjects


@login_required
def enrollment_form_view(request, pk):

    subjects = get_accessible_subjects(request.user)
    subject = get_object_or_404(subjects, pk=pk)

    screening = getattr(subject, "screening", None)

    # ✅ must have screening
    if not screening:
        return redirect("herbal:subjects-detail", pk=subject.pk)

    # ✅ must be eligible
    if not screening.eligible:
        return redirect("herbal:subjects-detail", pk=subject.pk)

    # =========================
    # ✅ GET EXISTING ENROLLMENT
    # =========================
    enrollment = getattr(screening, "enrollment", None)

    if request.method == "POST":

        form = EnrollmentForm(request.POST, instance=enrollment)

        if form.is_valid():

            enrollment_obj = form.save(commit=False)
            enrollment_obj.screening = screening
            enrollment_obj.save()

            # ✅ Only generate visits on CREATE
            if not enrollment:
                generate_visit_schedule(enrollment_obj)

            return redirect(
                "herbal:subjects-detail",
                pk=subject.pk
            )

    else:
        form = EnrollmentForm(instance=enrollment)

    context = {
        "form": form,
        "subject": subject,
        "screening": screening,
        "is_update": enrollment is not None
    }

    return render(
        request,
        "herbal/enrollments/enrollment_form.html",
        context
    )