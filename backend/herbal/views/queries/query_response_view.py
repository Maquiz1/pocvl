from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models.queries.query_model import DataQuery
from herbal.forms.query_form import QueryResponseForm


@login_required
def query_response_view(request, pk):

    query = get_object_or_404(DataQuery, pk=pk)

    if request.method == "POST":

        form = QueryResponseForm(request.POST, instance=query)

        if form.is_valid():

            query = form.save(commit=False)

            query.status = "answered"
            query.responded_by = request.user

            query.save()

            subject = query.visit.enrollment.screening.subject

            return redirect(
                "herbal:subjects-detail",
                pk=subject.pk
            )

    else:

        form = QueryResponseForm(instance=query)

    return render(
        request,
        "herbal/queries/query_response.html",
        {
            "form": form,
            "query": query
        }
    )