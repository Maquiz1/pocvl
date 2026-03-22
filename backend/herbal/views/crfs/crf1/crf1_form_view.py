from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.forms.crfs.crf1_form import CRF1Form
from herbal.services.visit_completion import update_visit_status
from django.db import IntegrityError
from herbal.forms.crfs.crf1_other_medications_form import CRF1OtherMedicalFormSet
from herbal.forms.crfs.crf1_nimregenin_form import CRF1NimregeninFormSet
from herbal.forms.crfs.crf1_other_herbal_form import CRF1OtherHerbalFormSet
from herbal.forms.crfs.crf1_radiotherapy_form import CRF1RadiotherapyFormSet
from herbal.forms.crfs.crf1_chemotherapy_form import CRF1ChemotherapyFormSet
from herbal.forms.crfs.crf1_surgery_form import CRF1SurgeryFormSet


@login_required
def crf1_form_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    # Only allow Day 0
    if visit.visit_day != "D0":
        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    # Check if CRF already exists
    crf_instance = getattr(visit, "crf1", None)

    if request.method == "POST":
        form = CRF1Form(request.POST, instance=crf_instance)

        other_formset = CRF1OtherMedicalFormSet(request.POST, instance=crf_instance, prefix="othermedicals")
        nimregenin_formset = CRF1NimregeninFormSet(request.POST, instance=crf_instance, prefix="nimregenins")
        herbal_formset = CRF1OtherHerbalFormSet(request.POST, instance=crf_instance, prefix="otherherbals")

        # ✅ FIXED HERE
        radio_formset = CRF1RadiotherapyFormSet(request.POST, instance=crf_instance, prefix="radiotherapies")
        chemo_formset = CRF1ChemotherapyFormSet(request.POST, instance=crf_instance, prefix="chemotherapies")
        surgery_formset = CRF1SurgeryFormSet(request.POST, instance=crf_instance, prefix="surgeries")

        if (
            form.is_valid() and
            other_formset.is_valid() and
            nimregenin_formset.is_valid() and
            herbal_formset.is_valid() and
            radio_formset.is_valid() and
            chemo_formset.is_valid() and
            surgery_formset.is_valid()
        ):
            crf = form.save(commit=False)
            crf.visit = visit

            try:
                crf.save()

                other_formset.instance = crf
                nimregenin_formset.instance = crf
                herbal_formset.instance = crf
                radio_formset.instance = crf
                chemo_formset.instance = crf
                surgery_formset.instance = crf

                other_formset.save()
                nimregenin_formset.save()
                herbal_formset.save()
                radio_formset.save()
                chemo_formset.save()
                surgery_formset.save()

                update_visit_status(visit)

                return redirect("herbal:subjects-detail", pk=visit.subject.pk)

            except IntegrityError:
                form.add_error(None, "CRF1 already exists for this visit.")

    else:
        form = CRF1Form(instance=crf_instance)
        other_formset = CRF1OtherMedicalFormSet(
            instance=crf_instance,
            prefix="othermedicals"   # ✅ ADD THIS
        )
        nimregenin_formset = CRF1NimregeninFormSet(
            instance=crf_instance,
            prefix="nimregenins"
        )
        herbal_formset = CRF1OtherHerbalFormSet(
            instance=crf_instance,
            prefix="otherherbals"
        )
        radio_formset = CRF1RadiotherapyFormSet(
            instance=crf_instance,
            prefix="radiotherapies"
        )

        chemo_formset = CRF1ChemotherapyFormSet(
            instance=crf_instance,
            prefix="chemotherapies"
        )

        surgery_formset = CRF1SurgeryFormSet(
            instance=crf_instance,
            prefix="surgeries"
        )

    return render(
        request,
        "herbal/crfs/crf1/crf1_form.html",
        {
            "form": form,
            "other_formset": other_formset,
            "nimregenin_formset": nimregenin_formset,
            "herbal_formset": herbal_formset,
            "radio_formset": radio_formset,
            "chemo_formset": chemo_formset,
            "surgery_formset": surgery_formset,
            "visit": visit,
            "is_update": crf_instance is not None
        }
    )