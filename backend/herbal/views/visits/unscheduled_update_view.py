from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models.visits.unschedule_visit_model import UnscheduledVisit
from herbal.forms.unscheduled_visit_form import UnscheduledVisitForm
from herbal.services.access_control import get_accessible_subjects


@login_required
def unscheduled_update_view(request, pk):

    unscheduled = get_object_or_404(
        UnscheduledVisit.objects.select_related("enrollment__screening__subject"),
        pk=pk
    )

    enrollment = unscheduled.enrollment
    subject = enrollment.screening.subject

    # 🔐 access control
    subjects = get_accessible_subjects(request.user)
    if subject not in subjects:
        return redirect("herbal:subjects-list")

    if request.method == "POST":
        form = UnscheduledVisitForm(
            request.POST,
            instance=unscheduled,
            enrollment=enrollment
        )

        if form.is_valid():
            form.save()
            return redirect("herbal:subjects-detail", pk=subject.pk)

    else:
        form = UnscheduledVisitForm(
            instance=unscheduled,
            enrollment=enrollment
        )

    return render(
        request,
        "herbal/visits/unscheduled_form.html",
        {
            "form": form,
            "subject": subject,
            "is_update": True,
        }
    )