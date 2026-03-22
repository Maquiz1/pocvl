from django.http import JsonResponse
from .models import Region, District, Ward


def search_regions(request):
    q = request.GET.get("q", "")
    data = Region.objects.filter(name__icontains=q)[:20]
    return JsonResponse([
        {"id": r.id, "text": r.name} for r in data
    ], safe=False)


def search_districts(request):
    q = request.GET.get("q", "")
    region_id = request.GET.get("region")

    qs = District.objects.all()

    if region_id:
        qs = qs.filter(region_id=region_id)

    if q:
        qs = qs.filter(name__icontains=q)

    qs = qs[:20]

    return JsonResponse([
        {"id": d.id, "text": d.name} for d in qs
    ], safe=False)


def search_wards(request):
    q = request.GET.get("q", "")
    district_id = request.GET.get("district")

    qs = Ward.objects.all()

    if district_id:
        qs = qs.filter(district_id=district_id)

    if q:
        qs = qs.filter(name__icontains=q)

    qs = qs[:20]

    return JsonResponse([
        {"id": w.id, "text": w.name} for w in qs
    ], safe=False)
    