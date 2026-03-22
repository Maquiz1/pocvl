from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import Subject, Screening
from herbal.forms.screening_form import ScreeningForm
from herbal.services.access_control import get_accessible_subjects


@login_required
def screening_form_view(request, pk):

    subjects = get_accessible_subjects(request.user)
    subject = get_object_or_404(subjects, pk=pk)

    # ✅ Get existing screening if available
    screening = Screening.objects.filter(subject=subject).first()

    if request.method == "POST":
        form = ScreeningForm(request.POST, instance=screening)

        if form.is_valid():
            screening_obj = form.save(commit=False)
            screening_obj.subject = subject
            screening_obj.save()

            form.save_m2m()  # ✅ THIS LINE FIXES EVERYTHING

            return redirect("herbal:subjects-detail", pk=subject.pk)

    else:
        form = ScreeningForm(instance=screening)

    context = {
        "form": form,
        "subject": subject,
        "is_update": screening is not None
    }

    return render(
        request,
        "herbal/screening/screening_form.html",
        context
    )