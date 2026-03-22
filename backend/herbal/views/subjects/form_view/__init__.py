from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from herbal.forms.subject_form import SubjectForm
from herbal.models.subjects import Subject
from herbal.services.access_control import get_accessible_subjects


@login_required
def subject_form_view(request, pk=None):

    # ✅ Determine if update or create
    if pk:
        subjects = get_accessible_subjects(request.user)
        subject = get_object_or_404(subjects, pk=pk)
    else:
        subject = None

    # ✅ POST
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)

        if form.is_valid():
            subject_obj = form.save(commit=False)

            # ✅ CREATE LOGIC
            if not subject:  
                if request.user.is_superuser:
                    if not subject_obj.site:
                        messages.error(request, "Please select a site.")
                        return render(
                            request,
                            "herbal/subjects/subject_form.html",
                            {"form": form, "subject": subject}
                        )
                else:
                    staff = request.user.staff_profile

                    if not staff.site:
                        messages.error(request, "You are not assigned to any site.")
                        return redirect("herbal:subjects-list")

                    subject_obj.site = staff.site

            # ✅ SAVE (both create & update)
            subject_obj.save()

            # redirect depending on action
            if pk:
                return redirect("herbal:subjects-detail", pk=subject_obj.pk)
            else:
                return redirect("herbal:subjects-list")

    # ✅ GET
    else:
        form = SubjectForm(instance=subject)

    return render(
        request,
        "herbal/subjects/subject_form.html",  # 👈 ONE template
        {
            "form": form,
            "subject": subject,
            "is_update": bool(pk),  # 👈 useful in template
        }
    )