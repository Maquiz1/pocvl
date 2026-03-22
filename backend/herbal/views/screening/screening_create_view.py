from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import Subject, Screening
from herbal.forms.screening_form import ScreeningForm
from herbal.services.access_control import get_accessible_subjects


@login_required
def screening_create_view(request, pk):

    subjects = get_accessible_subjects(request.user)
    subject = get_object_or_404(subjects, pk=pk)

    # ✅ SAFE check for existing screening
    if Screening.objects.filter(subject=subject).exists():
        return redirect("herbal:subjects-detail", pk=subject.pk)

    if request.method == "POST":
        form = ScreeningForm(request.POST)

        if form.is_valid():
            screening = form.save(commit=False)
            screening.subject = subject
            screening.save()

            return redirect("herbal:subjects-detail", pk=subject.pk)

    else:
        form = ScreeningForm()

    context = {
        "form": form,
        "subject": subject
    }

    return render(
        request,
        "herbal/screening/screening_form.html",
        context
    )