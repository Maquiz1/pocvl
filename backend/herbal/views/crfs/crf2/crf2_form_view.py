from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

from herbal.models import VisitSchedule
from herbal.models.crfs import CRF2
from herbal.models import CRF2OtherPhysclExam
from herbal.services.visit_completion import update_visit_status

from herbal.forms import CRF2Form


@login_required
def crf2_form_view(request, pk):
    visit = get_object_or_404(VisitSchedule, pk=pk)
    site = visit.site

    crf_instance = getattr(visit, "crf2", None)

    # 🔥 FORMSET
    OtherPhysclExamFormSet = inlineformset_factory(
        CRF2,
        CRF2OtherPhysclExam,
        fields=["system", "finding", "comments", "signifcnt"],
        extra=1,
        can_delete=True
    )

    if request.method == "POST":
        try:
            form = CRF2Form(request.POST, instance=crf_instance, site=site)
        except TypeError:
            form = CRF2Form(request.POST, instance=crf_instance)

        formset = OtherPhysclExamFormSet(request.POST, instance=crf_instance,prefix="other_physcl_exams"
)

        if form.is_valid() and formset.is_valid():
            crf = form.save(commit=False)
            crf.visit = visit
            crf.save()

            # 🔥 IMPORTANT: save formset AFTER crf exists
            formset.instance = crf
            formset.save()

            # # 🔥 Optional: clean if NOT YES
            # if not crf.physical_exams_other or crf.physical_exams_other.id != 1:
            #     crf.other_exams.all().delete()

            update_visit_status(visit)

            return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    else:
        try:
            form = CRF2Form(instance=crf_instance, site=site)
        except TypeError:
            form = CRF2Form(instance=crf_instance)

        formset = OtherPhysclExamFormSet(instance=crf_instance)

    return render(
        request,
        "herbal/crfs/crf2/crf2_form.html",
        {
            "form": form,
            "formset": formset,   # 🔥 pass to template
            "visit": visit,
            "is_update": crf_instance is not None,
        }
    )