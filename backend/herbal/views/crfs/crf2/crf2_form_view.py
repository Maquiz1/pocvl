from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.models.crfs import CRF2
from herbal.services.visit_completion import update_visit_status

from herbal.forms import (
    CRF2VitalsForm,
    CRF2SystemExamForm,
    CRF2OtherExamForm,
    CRF2FinalForm
)


FORMS = [
    CRF2VitalsForm,
    CRF2SystemExamForm,
    CRF2OtherExamForm,
    CRF2FinalForm
]


@login_required
def crf2_form_view(request, pk):
    visit = get_object_or_404(VisitSchedule, pk=pk)
    site = visit.site

    crf_instance = getattr(visit, "crf2", None)

    # step index (0-based)
    step = int(request.GET.get("step", 1)) - 1

    # safety clamp
    if step < 0:
        step = 0
    if step >= len(FORMS):
        step = len(FORMS) - 1

    # init session
    if "crf2_data" not in request.session:
        request.session["crf2_data"] = {}

        if crf_instance:
            for field in CRF2._meta.fields:
                name = field.name
                if name not in ["id", "visit"]:
                    value = getattr(crf_instance, name)

                    if hasattr(value, "pk"):
                        value = value.pk

                    request.session["crf2_data"][name] = value

    data = request.session["crf2_data"]

    FormClass = FORMS[step]

    def get_form(post_data=None):
        kwargs = {"initial": data}

        if post_data:
            kwargs["data"] = post_data

        try:
            return FormClass(**kwargs, site=site)
        except TypeError:
            return FormClass(**kwargs)

    if request.method == "POST":
        form = get_form(request.POST)

        if form.is_valid():
            cleaned = form.cleaned_data.copy()

            for key, value in cleaned.items():
                if hasattr(value, "pk"):
                    cleaned[key] = value.pk

            data.update(cleaned)
            request.session["crf2_data"] = data

            # LAST STEP
            if step + 1 == len(FORMS):

                if crf_instance:
                    for key, value in data.items():
                        setattr(crf_instance, key, value)
                    crf = crf_instance
                else:
                    crf = CRF2(**data)
                    crf.visit = visit

                crf.save()

                # cleanup
                del request.session["crf2_data"]

                update_visit_status(visit)

                return redirect("herbal:subjects-detail", pk=visit.subject.pk)

            return redirect(f"?step={step+2}")

    else:
        form = get_form()

    # ✅ display values
    step_display = step + 1
    total_steps = len(FORMS)
    progress = int((step_display / total_steps) * 100)

    return render(
        request,
        "herbal/crfs/crf2/crf2_form.html",
        {
            "form": form,
            "visit": visit,
            "step": step_display,
            "total_steps": total_steps,
            "progress": progress,
            "is_update": crf_instance is not None,
        }
    )