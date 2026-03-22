from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from herbal.forms.subject_form import SubjectForm

@login_required
def subject_create_view(request):

    if request.method == "POST":
        form = SubjectForm(request.POST)

        if form.is_valid():
            subject = form.save(commit=False)

            if request.user.is_superuser:
                if not subject.site:
                    messages.error(request, "Please select a site.")
                    return render(request, "herbal/subjects/subject_create.html", {"form": form})
            else:
                staff = request.user.staff_profile

                if not staff.site:
                    messages.error(request, "You are not assigned to any site.")
                    return redirect("herbal:subjects-list")

                subject.site = staff.site

            subject.save()
            return redirect("herbal:subjects-list")

    else:
        form = SubjectForm()

    return render(
        request,
        "herbal/subjects/subject_create.html",
        {"form": form},
    )