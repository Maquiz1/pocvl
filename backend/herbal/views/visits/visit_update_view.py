# herbal/views/visits/visit_update_view.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.forms.visit_start_form import VisitStartForm


@login_required
def visit_update_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    if request.method == "POST":
        form = VisitStartForm(request.POST, instance=visit)

        if form.is_valid():
            visit = form.save(commit=False)

            visit.save()

            return redirect(
                "herbal:subjects-detail",
                pk=visit.subject.pk
            )

    else:
        form = VisitStartForm(instance=visit)

    return render(
        request,
        "herbal/visits/visit_form.html",
        {
            "form": form,
            "visit": visit,
            "is_edit": bool(visit.actual_visit_date),
        }
    )