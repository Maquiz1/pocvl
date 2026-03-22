from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.models.crfs.crf1.crf1_model import CRF1
from herbal.forms.crfs.crf1_form import CRF1Form


@login_required
def crf1_update_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    crf = get_object_or_404(CRF1, visit=visit)

    if request.method == "POST":

        form = CRF1Form(request.POST, instance=crf)

        if form.is_valid():

            form.save()

            return redirect(
                "herbal:subjects-detail",
                pk=visit.subject.pk
            )

    else:

        form = CRF1Form(instance=crf)

    return render(
        request,
        "herbal/crfs/crf1/crf1_form.html",
        {
            "form": form,
            "visit": visit,
            "is_update": True,
        }
    )