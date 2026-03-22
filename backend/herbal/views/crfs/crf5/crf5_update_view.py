from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models.crfs.crf5.crf5_model import CRF5
from herbal.forms.crfs.crf5_form import CRF5Form


@login_required
def crf5_update_view(request, pk):

    crf = get_object_or_404(CRF5, pk=pk)

    enrollment = crf.enrollment

    subject = enrollment.screening.subject

    if request.method == "POST":

        form = CRF5Form(request.POST, instance=crf,enrollment=enrollment)

        if form.is_valid():

            form.save()

            return redirect(
                "herbal:subjects-detail",
                pk=subject.pk
            )

    else:

        form = CRF5Form(instance=crf,enrollment=enrollment)

    return render(
        request,
        "herbal/crfs/crf5/crf5_form.html",
        {
            "form": form,
            "crf": crf,
            "enrollment": enrollment,
            "subject": subject,
            "is_update": True,
        }
    )