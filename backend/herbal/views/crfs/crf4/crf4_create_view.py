from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.forms.crfs.crf4_form import CRF4Form
from herbal.services.visit_completion import update_visit_status

@login_required
def crf4_create_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    if hasattr(visit, "crf4"):
        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    if request.method == "POST":

        form = CRF4Form(request.POST)

        if form.is_valid():

            crf = form.save(commit=False)

            crf.visit = visit

            crf.save()
            update_visit_status(visit)

            return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    else:

        form = CRF4Form()

    return render(
        request,
        "herbal/crfs/crf4/crf4_form.html",
        {
            "form": form,
            "visit": visit
        }
    )