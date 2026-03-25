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
        .prefetch_related("screening__enrollment__visits")
        .order_by("-created_at")
    )

    search = request.GET.get("search")
    status = request.GET.get("status")

    # ---------------- SEARCH ----------------
    subjects = apply_search(
        subjects,
        search,
        ["subject_id", "first_name", "last_name", "phone_number",
         "other_phone", "hid", "idn", "other_id"]
    )

    # ---------------- FILTERS ----------------
    subjects = apply_filters(subjects, request, ["site"])

    # ---------------- PROGRESS ANNOTATION ----------------
    subjects = subjects.annotate(
        progress_percent=Case(

            # 🔴 Terminated (highest priority)
            When(
                screening__enrollment__termination__isnull=False,
                then=Value(100)
            ),

            # 🟡 Visits exist
            When(
                screening__enrollment__visits__isnull=False,
                then=Value(80)
            ),

            # 🔵 Enrolled
            When(
                screening__enrollment__isnull=False,
                then=Value(60)
            ),

            # ⚪ Screened
            When(
                screening__isnull=False,
                then=Value(40)
            ),

            # ⚪ Registered
            When(
                screening__isnull=True,
                then=Value(20)
            ),

            output_field=IntegerField()
        )
    ).distinct()

    # ---------------- COUNTS ----------------
    counts = subjects.aggregate(

        total_subjects=Count("id", distinct=True),

        screened_count=Count(
            "id",
            filter=Q(screening__isnull=False),
            distinct=True
        ),

        eligible_count=Count(
            "id",
            filter=Q(screening__eligible=True),
            distinct=True
        ),

        enrolled_count=Count(
            "id",
            filter=Q(screening__enrollment__isnull=False),
            distinct=True
        ),

        visits_count=Count(
            "id",
            filter=Q(screening__enrollment__visits__isnull=False),
            distinct=True
        ),

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

    # ---------------- STATUS FILTER ----------------
    if status == "registered":
        subjects = subjects.filter(screening__isnull=True)

    elif status == "screened":
        subjects = subjects.filter(
            screening__isnull=False,
            screening__enrollment__isnull=True,
            screening__eligible=False
        )

    elif status == "eligible":
        subjects = subjects.filter(
            screening__eligible=True,
            screening__enrollment__isnull=True
        )

    elif status == "enrolled":
        subjects = subjects.filter(
            screening__enrollment__isnull=False,
            screening__enrollment__visits__isnull=True,
            screening__enrollment__termination__isnull=True
        )

    elif status == "visits":
        subjects = subjects.filter(
            screening__enrollment__visits__isnull=False,
            screening__enrollment__termination__isnull=True
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
        "visits_count": counts["visits_count"],
        "terminated_count": counts["terminated_count"],
        "ltf_count": counts["ltf_count"],
    }

    return render(
        request,
        "herbal/subjects/subject_list.html",
        context
    )