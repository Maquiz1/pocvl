from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import Subject


@login_required
def crf_list_view(request):

    crfs = [
        {"name": "CRF1", "url": "herbal:crf1-list"},
        {"name": "CRF2", "url": "herbal:crf2-list"},
        {"name": "CRF3", "url": "herbal:crf3-form"},
        {"name": "CRF4", "url": "herbal:crf4-create"},
        {"name": "CRF7", "url": "herbal:crf7-form"},
    ]

    return render(request, "herbal/crfs/crf_list.html", {"crfs": crfs})

    # context = {
    #     "subject": subject,
    #     "visits": visits,
    # }

    # return render(
    #     request,
    #     "herbal/crfs/crf_overview.html",
    #     context
    # )