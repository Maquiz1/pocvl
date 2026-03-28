from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.models.crfs.crf3.crf3_model import CRF3
from herbal.forms.crfs.crf3_form import CRF3Form
from herbal.services.visit_completion import update_visit_status


@login_required
def crf3_form_view(request, pk):
    visit = get_object_or_404(VisitSchedule, pk=pk)

    # Try to get existing CRF3 instance, or None if not created yet
    crf_instance = getattr(visit, "crf3", None)

    if request.method == "POST":
        form = CRF3Form(request.POST, instance=crf_instance)

        if form.is_valid():
            crf = form.save(commit=False)
            crf.visit = visit
            crf.save()

            update_visit_status(visit)

            return redirect("herbal:subjects-detail", pk=visit.subject.pk)
    else:
        form = CRF3Form(instance=crf_instance)

    return render(
        request,
        "herbal/crfs/crf3/crf3_form.html",
        {
            "form": form,
            "visit": visit,
            "is_update": crf_instance is not None,
        }
    )
