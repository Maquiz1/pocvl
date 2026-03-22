from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import Enrollment
from herbal.forms.crfs.crf5_form import CRF5Form


@login_required
def crf5_create_view(request, pk):

    enrollment = get_object_or_404(Enrollment, pk=pk)

    subject = enrollment.screening.subject

    if request.method == "POST":

        form = CRF5Form(request.POST, enrollment=enrollment)
        if form.is_valid():

            crf = form.save(commit=False)

            crf.enrollment = enrollment

            crf.save()

            return redirect(
                "herbal:subjects-detail",
                pk=subject.pk
            )

    else:

        form = CRF5Form(enrollment=enrollment)
        
    return render(
        request,
        "herbal/crfs/crf5/crf5_form.html",
        {
            "form": form,
            "enrollment": enrollment,
            "subject": subject,
        }
    )