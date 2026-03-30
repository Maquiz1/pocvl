from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.models.crfs.crf4.crf4_model import CRF4
from herbal.forms.crfs.crf4_form import CRF4Form
from herbal.services.visit_completion import update_visit_status


@login_required
def crf4_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    # Try to get existing CRF4 (if exists → update, else → create)
    crf = getattr(visit, "crf4", None)

    if request.method == "POST":
        form = CRF4Form(request.POST, instance=crf)

        if form.is_valid():
            crf_obj = form.save(commit=False)
            crf_obj.visit = visit
            crf_obj.save()

            update_visit_status(visit)

            return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    else:
        form = CRF4Form(instance=crf)

    return render(
        request,
        "herbal/crfs/crf4/crf4_form.html",
        {
            "form": form,
            "visit": visit,
            "is_update": crf is not None,  # useful in template
        }
    )