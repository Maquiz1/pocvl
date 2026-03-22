from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models.queries.query_model import DataQuery


@login_required
def query_close_view(request, pk):

    query = get_object_or_404(DataQuery, pk=pk)

    query.status = "closed"

    query.save()

    subject = query.visit.enrollment.screening.subject

    return redirect(
        "herbal:subjects-detail",
        pk=subject.pk
    )