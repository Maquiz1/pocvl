from herbal.models.visits.visit_schedule_model import VisitSchedule
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


from django.utils import timezone

@login_required
def visit_mark_pending(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    # ❌ Do not allow NA to be changed
    if visit.status == "na":
        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    # ✅ Only allow missed → pending
    if visit.status == "missed":

        visit.status = "pending"
        visit.missed_reason = None
        visit.save()

    return redirect("herbal:subjects-detail", pk=visit.subject.pk)