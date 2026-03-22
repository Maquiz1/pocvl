from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.models.crfs.crf4.crf4_model import CRF4
from herbal.forms.crfs.crf4_form import CRF4Form


@login_required
def crf4_update_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    crf = get_object_or_404(CRF4, visit=visit)

    if request.method == "POST":

        form = CRF4Form(request.POST, instance=crf)

        if form.is_valid():

            form.save()

            return redirect(
                "herbal:subjects-detail",
                pk=visit.subject.pk
            )

    else:

        form = CRF4Form(instance=crf)

    return render(
        request,
        "herbal/crfs/crf4/crf4_form.html",
        {
            "form": form,
            "visit": visit,
            "is_update": True,
        }
    )