from herbal.models.visits.visit_schedule_model import VisitSchedule
from choices.models import MissedVisitReason  # 👈 ADD THIS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def visit_mark_missed(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    # ❌ DO NOT allow NA visits to be changed
    if visit.status == "na":
        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    if request.method == "POST":

        if visit.status == "pending":

            reason_code = request.POST.get("reason")
            comment = request.POST.get("comment")

            # ✅ GET actual model instance
            reason = MissedVisitReason.objects.get(code=reason_code)

            visit.status = "missed"
            visit.missed_reason = reason   # ✅ FIXED
            visit.missed_comment = comment
            visit.save()

        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    return render(
        request,
        "herbal/visits/mark_missed.html",
        {"visit": visit}
    )