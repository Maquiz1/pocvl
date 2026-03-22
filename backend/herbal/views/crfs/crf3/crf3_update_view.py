from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.models.crfs.crf3.crf3_model import CRF3
from herbal.forms.crfs.crf3_form import CRF3Form


@login_required
def crf3_update_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    crf = get_object_or_404(CRF3, visit=visit)

    if request.method == "POST":

        form = CRF3Form(request.POST, instance=crf)

        if form.is_valid():

            form.save()

            return redirect(
                "herbal:subjects-detail",
                pk=visit.subject.pk
            )

    else:

        form = CRF3Form(instance=crf)

    return render(
        request,
        "herbal/crfs/crf3/crf3_form.html",
        {
            "form": form,
            "visit": visit,
            "is_update": True,
        }
    )