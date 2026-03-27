# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from herbal.models import VisitSchedule
from herbal.forms.crfs.crf1_form import CRF1Form
from herbal.forms.crfs.crf1_other_medications_form import CRF1OtherMedicalFormSet
from herbal.services.visit_completion import update_visit_status

@login_required
def test_other_medicals_view(request, pk):
    print("METHOD:", request.method)

    visit = get_object_or_404(VisitSchedule, pk=pk)

    # Only allow Day 0
    if visit.visit_day.code != "D0":
        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    # Check if CRF already exists
    crf_instance = getattr(visit, "crf1", None)

    if request.method == "POST":
        form = CRF1Form(request.POST, instance=crf_instance)
        other_formset = CRF1OtherMedicalFormSet(
            request.POST,
            instance=crf_instance,
            prefix="othermedicals"
        )

        if form.is_valid() and other_formset.is_valid():
            crf = form.save(commit=False)
            crf.visit = visit
            try:
                crf.save()
                other_formset.instance = crf
                other_formset.save()
                update_visit_status(visit)
                return redirect("herbal:subjects-detail", pk=visit.subject.pk)
            except IntegrityError:
                form.add_error(None, "CRF1 already exists for this visit.")
    else:
        form = CRF1Form(instance=crf_instance)
        other_formset = CRF1OtherMedicalFormSet(
            instance=crf_instance,
            prefix="othermedicals"
        )

    return render(
        request,
        "herbal/crfs/crf1/crf1_form.html",
        {
            "form": form,
            "other_formset": other_formset,
            "visit": visit,
            "is_update": crf_instance is not None,
        }
    )
