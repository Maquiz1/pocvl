from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from herbal.models import VisitSchedule
from herbal.forms.crfs.crf2.crf2_form import CRF2Form
from herbal.services.visit_completion import update_visit_status
from herbal.forms.crfs.crf2.crf2_other_form import CRF2OtherPhysclExamFormSet


@login_required
def crf2_form_view(request, pk):
    visit = get_object_or_404(VisitSchedule, pk=pk)
    crf_instance = getattr(visit, "crf2", None)

    if request.method == "POST":
        form = CRF2Form(request.POST, instance=crf_instance)

        if form.is_valid():
            crf = form.save(commit=False)
            crf.visit = visit

            try:
                crf.save()

                # Always bind formset with the saved instance
                exam_formset = CRF2OtherPhysclExamFormSet(
                    request.POST, instance=crf, prefix="otherexams"
                )

                if exam_formset.is_valid():
                    exam_formset.save()
                    update_visit_status(visit)
                    return redirect("herbal:subjects-detail", pk=visit.subject.pk)
                else:
                    print("FORMSET ERRORS:", exam_formset.errors)

            except IntegrityError:
                form.add_error(None, "CRF2 already exists for this visit.")
                exam_formset = CRF2OtherPhysclExamFormSet(
                    request.POST, instance=crf_instance, prefix="otherexams"
                )
        else:
            # Form invalid → still bind formset so template can re-render
            exam_formset = CRF2OtherPhysclExamFormSet(
                request.POST, instance=crf_instance, prefix="otherexams"
            )

    else:  # GET request
        form = CRF2Form(instance=crf_instance)
        exam_formset = CRF2OtherPhysclExamFormSet(
            instance=crf_instance, prefix="otherexams"
        )

    return render(
        request,
        "herbal/crfs/crf2/crf2_form.html",
        {
            "form": form,
            "exam_formset": exam_formset,
            "visit": visit,
            "is_update": crf_instance is not None,
        },
    )
