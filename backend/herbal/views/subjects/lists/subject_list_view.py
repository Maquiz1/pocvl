from django.shortcuts import render
from django.db.models import Case, When, Value, IntegerField, Count, Q
from herbal.models import Subject
from utils.pagination import paginate_queryset
from utils.filters import apply_search, apply_filters
from sites.models import Site


def subject_list_view(request):

    # ---------------- BASE QUERYSET ----------------
    subjects = (
        Subject.objects.for_user(request.user)
        .select_related("site", "screening", "screening__enrollment")
        .order_by("-created_at")
    )

    search = request.GET.get("search")
    status = request.GET.get("status")

    # ---------------- SEARCH ----------------
    subjects = apply_search(
        subjects,
        search,
        ["subject_id", "first_name", "last_name", "phone"]
    )

    # ---------------- FILTERS ----------------
    subjects = apply_filters(subjects, request, ["site"])

    # ---------------- ANNOTATION (PROGRESS) ----------------
    subjects = subjects.annotate(
        progress_percent=Case(
            When(screening__isnull=True, then=Value(20)),   # Registered
            When(
                screening__isnull=False,
                screening__enrollment__isnull=True,
                then=Value(60)
            ),  # Screened / Eligible
            When(screening__enrollment__isnull=False, then=Value(100)),  # Enrolled
            output_field=IntegerField()
        )
    )

    # ---------------- COUNTS (CLINICAL CORRECT) ----------------
    counts = subjects.aggregate(

        # Registered = all subjects
        total_subjects=Count("id", distinct=True),

        # Screened (has screening)
        screened_count=Count(
            "id",
            filter=Q(screening__isnull=False),
            distinct=True
        ),

        # Eligible (screening.eligible=True)
        eligible_count=Count(
            "id",
            filter=Q(screening__eligible=True),
            distinct=True
        ),

        # Enrolled
        enrolled_count=Count(
            "id",
            filter=Q(screening__enrollment__isnull=False),
            distinct=True
        ),

        # Terminated (CRF6 exists)
        terminated_count=Count(
            "id",
            filter=Q(screening__enrollment__termination__isnull=False),
            distinct=True
        ),
        
        ltf_count=Count(
            "id",
            filter=Q(
                screening__enrollment__termination__reason="ltf"
            ),
            distinct=True
        ),
    )

    # ---------------- STATUS FILTER (TABLE ONLY) ----------------
    if status == "registered":
        subjects = subjects.filter(screening__isnull=True)

    elif status == "screened":
        subjects = subjects.filter(
            screening__isnull=False,
            screening__eligible=False
        )

    elif status == "eligible":
        subjects = subjects.filter(
            screening__eligible=True,
            screening__enrollment__isnull=True
        )

    elif status == "enrolled":
        subjects = subjects.filter(
            screening__enrollment__isnull=False
        )

    elif status == "terminated":
        subjects = subjects.filter(
            screening__enrollment__termination__isnull=False
        )
        
    elif status == "ltf":
        subjects = subjects.filter(
            screening__enrollment__termination__reason="ltf"
        )

    # ---------------- PAGINATION ----------------
    page_obj = paginate_queryset(request, subjects)

    # ---------------- FILTER DROPDOWNS ----------------
    sites = Site.objects.all()

    # ---------------- CONTEXT ----------------
    context = {
        "page_obj": page_obj,
        "search": search,
        "status": status,
        "sites": sites,

        "total_subjects": counts["total_subjects"],
        "screened_count": counts["screened_count"],
        "eligible_count": counts["eligible_count"],
        "enrolled_count": counts["enrolled_count"],
        "terminated_count": counts["terminated_count"],
        "ltf_count": counts["ltf_count"],
    }

    return render(
        request,
        "herbal/subjects/subject_list.html",
        context
    )