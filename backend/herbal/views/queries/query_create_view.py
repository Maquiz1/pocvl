from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models.visits.visit_schedule_model import VisitSchedule
from herbal.forms.query_form import QueryCreateForm


@login_required
def query_create_view(request, visit_id):

    visit = get_object_or_404(VisitSchedule, pk=visit_id)

    if request.method == "POST":

        form = QueryCreateForm(request.POST)

        if form.is_valid():

            query = form.save(commit=False)

            query.visit = visit
            query.raised_by = request.user

            query.save()

            subject = visit.enrollment.screening.subject

            return redirect(
                "herbal:subjects-detail",
                pk=subject.pk
            )

    else:

        form = QueryCreateForm()

    return render(
        request,
        "herbal/queries/query_form.html",
        {
            "form": form,
            "visit": visit
        }
    )