from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.models.crfs import CRF2
from herbal.services.visit_completion import update_visit_status

from herbal.forms import CRF2Form


@login_required
def crf2_form_view(request, pk):
    visit = get_object_or_404(VisitSchedule, pk=pk)
    site = visit.site

    # Check if CRF already exists (for update)
    crf_instance = getattr(visit, "crf2", None)

    # Initialize form
    if request.method == "POST":
        try:
            form = CRF2Form(request.POST, instance=crf_instance, site=site)
        except TypeError:
            form = CRF2Form(request.POST, instance=crf_instance)

        if form.is_valid():
            crf = form.save(commit=False)
            crf.visit = visit
            crf.save()

            # update visit completion
            update_visit_status(visit)

            return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    else:
        try:
            form = CRF2Form(instance=crf_instance, site=site)
        except TypeError:
            form = CRF2Form(instance=crf_instance)

    return render(
        request,
        "herbal/crfs/crf2/crf2_form.html",
        {
            "form": form,
            "visit": visit,
            "is_update": crf_instance is not None,
        }
    )