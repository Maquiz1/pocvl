from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.models.crfs.crf7.crf7_model import CRF7
from herbal.forms.crfs.crf7_form import CRF7Form


@login_required
def crf7_update_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    crf = get_object_or_404(CRF7, visit=visit)

    if request.method == "POST":

        form = CRF7Form(request.POST, instance=crf)

        if form.is_valid():

            form.save()

            return redirect(
                "herbal:subjects-detail",
                pk=visit.subject.pk
            )

    else:

        form = CRF7Form(instance=crf)

    return render(
        request,
        "herbal/crfs/crf7/crf7_form.html",
        {
            "form": form,
            "visit": visit,
            "is_update": True,
        }
    )