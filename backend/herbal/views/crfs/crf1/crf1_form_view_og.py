from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from herbal.models import VisitSchedule
from herbal.forms.crfs.crf1_form import CRF1Form
from herbal.services.visit_completion import update_visit_status

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
    if visit.visit_day.code != "D0":
        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    crf_instance = getattr(visit, "crf1", None)

    # =========================
    # POST
    # =========================
    if request.method == "POST":

        form = CRF1Form(request.POST, instance=crf_instance)

        # STEP 1: Validate main form ONLY
        if form.is_valid():

            crf = form.save(commit=False)
            crf.visit = visit

            try:
                crf.save()

                # STEP 2: NOW bind formsets with correct instance
                other_formset = CRF1OtherMedicalFormSet(request.POST, instance=crf, prefix="othermedicals")
                nimregenin_formset = CRF1NimregeninFormSet(request.POST, instance=crf, prefix="nimregenins")
                herbal_formset = CRF1OtherHerbalFormSet(request.POST, instance=crf, prefix="otherherbals")
                radio_formset = CRF1RadiotherapyFormSet(request.POST, instance=crf, prefix="radiotherapies")
                chemo_formset = CRF1ChemotherapyFormSet(request.POST, instance=crf, prefix="chemotherapies")
                surgery_formset = CRF1SurgeryFormSet(request.POST, instance=crf, prefix="surgeries")

                # STEP 3: Validate formsets AFTER correct binding
                if (
                    other_formset.is_valid() and
                    nimregenin_formset.is_valid() and
                    herbal_formset.is_valid() and
                    radio_formset.is_valid() and
                    chemo_formset.is_valid() and
                    surgery_formset.is_valid()
                ):
                    other_formset.save()
                    nimregenin_formset.save()
                    herbal_formset.save()
                    radio_formset.save()
                    chemo_formset.save()
                    surgery_formset.save()

                    update_visit_status(visit)

                    return redirect("herbal:subjects-detail", pk=visit.subject.pk)

                else:
                    # DEBUG (optional but useful)
                    print("FORMSET ERRORS:")
                    print(other_formset.errors)
                    print(nimregenin_formset.errors)

            except IntegrityError:
                form.add_error(None, "CRF1 already exists for this visit.")

        else:
            # If form invalid, still need formsets to re-render
            other_formset = CRF1OtherMedicalFormSet(request.POST, instance=crf_instance, prefix="othermedicals")
            nimregenin_formset = CRF1NimregeninFormSet(request.POST, instance=crf_instance, prefix="nimregenins")
            herbal_formset = CRF1OtherHerbalFormSet(request.POST, instance=crf_instance, prefix="otherherbals")
            radio_formset = CRF1RadiotherapyFormSet(request.POST, instance=crf_instance, prefix="radiotherapies")
            chemo_formset = CRF1ChemotherapyFormSet(request.POST, instance=crf_instance, prefix="chemotherapies")
            surgery_formset = CRF1SurgeryFormSet(request.POST, instance=crf_instance, prefix="surgeries")

    # =========================
    # GET
    # =========================
    else:
        form = CRF1Form(instance=crf_instance)

        other_formset = CRF1OtherMedicalFormSet(instance=crf_instance, prefix="othermedicals")
        nimregenin_formset = CRF1NimregeninFormSet(instance=crf_instance, prefix="nimregenins")
        herbal_formset = CRF1OtherHerbalFormSet(instance=crf_instance, prefix="otherherbals")
        radio_formset = CRF1RadiotherapyFormSet(instance=crf_instance, prefix="radiotherapies")
        chemo_formset = CRF1ChemotherapyFormSet(instance=crf_instance, prefix="chemotherapies")
        surgery_formset = CRF1SurgeryFormSet(instance=crf_instance, prefix="surgeries")

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