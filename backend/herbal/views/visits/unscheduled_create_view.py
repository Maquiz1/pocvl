from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import Enrollment
from herbal.forms.unscheduled_visit_form import UnscheduledVisitForm
from herbal.services.access_control import get_accessible_subjects


@login_required
def unscheduled_create_view(request, pk):

    # pk = enrollment id
    enrollment = get_object_or_404(Enrollment, pk=pk)

    subject = enrollment.screening.subject

    # 🔐 access control
    subjects = get_accessible_subjects(request.user)
    if subject not in subjects:
        return redirect("herbal:subjects-list")

    if request.method == "POST":
        form = UnscheduledVisitForm(
            request.POST,
            enrollment=enrollment
        )

        if form.is_valid():
            unscheduled = form.save(commit=False)
            unscheduled.enrollment = enrollment
            unscheduled.save()

            return redirect("herbal:subjects-detail", pk=subject.pk)

    else:
        form = UnscheduledVisitForm(enrollment=enrollment)

    return render(
        request,
        "herbal/visits/unscheduled_form.html",
        {
            "form": form,
            "subject": subject,
            "is_update": False,
        }
    )