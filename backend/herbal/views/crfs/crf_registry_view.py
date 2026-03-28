from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from herbal.models.crfs.crf1.crf1_model import CRF1
from herbal.models.crfs.crf2.crf2_model import CRF2
from herbal.models.crfs.crf3.crf3_model import CRF3
from herbal.models.crfs.crf4.crf4_model import CRF4
from herbal.models.crfs.crf5.crf5_model import CRF5
from herbal.models.crfs.crf6.crf6_model import CRF6
from herbal.models.crfs.crf7.crf7_model import CRF7


@login_required
def crf_registry_view(request):

    crfs = [
        {
            "name": "CRF1",
            "count": CRF1.objects.count(),
            "recent": CRF1.objects.select_related("visit")[:5],
        },
        {
            "name": "CRF2",
            "count": CRF2.objects.count(),
            "recent": CRF2.objects.select_related("visit")[:5],
        },
        {
            "name": "CRF3",
            "count": CRF3.objects.count(),
            "recent": CRF3.objects.select_related("visit")[:5],
        },
        {
            "name": "CRF4",
            "count": CRF4.objects.count(),
            "recent": CRF4.objects.select_related("visit")[:5],
        },
        {
            "name": "CRF5",
            "count": CRF5.objects.count(),
            "recent": CRF5.objects.select_related("enrollment", "after_visit")[:5],
        },
        {
            "name": "CRF6",
            "count": CRF6.objects.count(),
            "recent": CRF6.objects.select_related("enrollment")[:5],  # ✅ FIX
        },
        {
            "name": "CRF7",
            "count": CRF7.objects.count(),
            "recent": CRF7.objects.select_related("visit")[:5],
        },
    ]

    return render(
        request,
        "herbal/crfs/crf_registry.html",
        {"crfs": crfs}
    )