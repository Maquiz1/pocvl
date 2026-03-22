from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.forms.crfs.crf3_form import CRF3Form
from herbal.services.visit_completion import update_visit_status

@login_required
def crf3_create_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    if hasattr(visit, "crf3"):
        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    if request.method == "POST":

        form = CRF3Form(request.POST)

        if form.is_valid():

            crf = form.save(commit=False)

            crf.visit = visit

            crf.save()
            update_visit_status(visit)

            return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    else:

        form = CRF3Form()

    return render(
        request,
        "herbal/crfs/crf3/crf3_form.html",
        {
            "form": form,
            "visit": visit
        }
    )