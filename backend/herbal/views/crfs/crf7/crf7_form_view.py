from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.models.crfs.crf7.crf7_model import CRF7
from herbal.forms.crfs.crf7_form import CRF7Form
from herbal.services.visit_completion import update_visit_status


@login_required
def crf7_form_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    # ✅ get existing or None
    crf_instance = getattr(visit, "crf7", None)

    if request.method == "POST":

        form = CRF7Form(request.POST, instance=crf_instance)

        # 🔥 IMPORTANT (same as CRF3)
        form.instance.visit = visit

        if form.is_valid():

            crf = form.save(commit=False)
            crf.visit = visit
            crf.save()

            update_visit_status(visit)

            return redirect(
                "herbal:subjects-detail",
                pk=visit.subject.pk
            )

    else:

        form = CRF7Form(instance=crf_instance)

    return render(
        request,
        "herbal/crfs/crf7/crf7_form.html",
        {
            "form": form,
            "visit": visit,
            "is_update": crf_instance is not None,
        }
    )