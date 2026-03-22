from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from herbal.forms.subject_form import SubjectForm
from herbal.models import Subject
from herbal.services.access_control import get_accessible_subjects


@login_required
def subject_form_view(request, pk=None):

    if pk:
        subjects = get_accessible_subjects(request.user)
        subject = get_object_or_404(subjects, pk=pk)
    else:
        subject = None

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)

        # ❗ HANDLE INVALID FORM FIRST
        if not form.is_valid():
            return render(
                request,
                "herbal/subjects/subject_form.html",
                {
                    "form": form,
                    "subject": subject,
                    "is_update": bool(pk),
                }
            )

        subject_obj = form.save(commit=False)

        # CREATE LOGIC
        if not subject:
            if request.user.is_superuser:
                if not subject_obj.site:
                    messages.error(request, "Please select a site.")
                    return render(
                        request,
                        "herbal/subjects/subject_form.html",
                        {
                            "form": form,
                            "subject": subject,
                            "is_update": bool(pk),
                        }
                    )
            else:
                staff = request.user.staff_profile

                if not staff.site:
                    messages.error(request, "You are not assigned to any site.")
                    return redirect("herbal:subjects-list")

                subject_obj.site = staff.site

        subject_obj.save()

        return redirect("herbal:subjects-list")

    else:
        form = SubjectForm(instance=subject)

    return render(
        request,
        "herbal/subjects/subject_form.html",
        {
            "form": form,
            "subject": subject,
            "is_update": bool(pk),
        }
    )