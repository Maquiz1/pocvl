from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Sum

from herbal.models import Subject, Screening, Enrollment, VisitSchedule
from herbal.models.crfs.crf5.crf5_model import CRF5
from herbal.models import StudyTarget


@login_required
def dashboard_view(request):

    user = request.user
    profile = user.staff_profile
    role = profile.role

    # =========================
    # SUBJECT FILTERING
    # =========================
    subjects = Subject.objects.all()

    if role in ["data_clerk", "coordinator"]:
        subjects = subjects.filter(site=profile.site)

    elif role in ["monitor", "reviewer", "pi"]:
        subjects = subjects.filter(site__in=profile.assigned_sites.all())

    screenings = Screening.objects.filter(subject__in=subjects)
    enrollments = Enrollment.objects.filter(screening__subject__in=subjects)
    visits = VisitSchedule.objects.filter(
        enrollment__screening__subject__in=subjects
    )

    today = timezone.now().date()

    # =========================
    # KPI
    # =========================
    total_subjects = subjects.count()
    screened_subjects = screenings.count()
    enrolled_subjects = enrollments.count()

    scheduled_visits = visits.count()
    completed_visits = visits.filter(status="completed").count()
    missed_visits = visits.filter(status="missed").count()

    overdue_visits = visits.filter(
        status="pending",
        scheduled_date__lt=today
    ).count()

    adverse_events = CRF5.objects.filter(
        enrollment__screening__subject__in=subjects
    ).count()

    # =========================
    # 🎯 TARGET FILTERING (IMPORTANT FIX)
    # =========================
    targets = StudyTarget.objects.all()
    if role in ["data_clerk", "coordinator"]:
        targets = targets.filter(site=profile.site)

    elif role in ["monitor", "reviewer", "pi"]:
        targets = targets.filter(site__in=profile.assigned_sites.all())

    # =========================
    # 🎯 OVERALL
    # =========================
    total_target = targets.aggregate(
        total=Sum("target_enrollment")
    )["total"] or 0
    overall_percent = int((enrolled_subjects / total_target) * 100) if total_target > 0 else 0

    # =========================
    # 🏥 SITE PROGRESS (FIXED: use targets)
    # =========================
    site_targets = targets.values(
        "site__name"
    ).annotate(
        target=Sum("target_enrollment")
    )
    
    site_enrollments = Enrollment.objects.filter(
        screening__subject__in=subjects
    ).values(
        "screening__subject__site__name"
    ).annotate(
        enrolled=Count("id")
    )
    
    enrolled_map = {
        e["screening__subject__site__name"]: e["enrolled"]
        for e in site_enrollments
    }

    site_progress = []
    for s in site_targets:
        name = s["site__name"]
        site_progress.append({
            "site__name": name,
            "target": s["target"],
            "enrolled": enrolled_map.get(name, 0)
        })

    # =========================
    # 🧬 CANCER PROGRESS (FIXED)
    # =========================
    # 1. TARGETS (no joins → correct)
    target_data = targets.values(
        "cancer_type__name"
    ).annotate(
        target=Sum("target_enrollment")
    )

    # 2. ENROLLMENTS (separate query)
    enrolled_data = Enrollment.objects.filter(
        screening__subject__in=subjects
    ).values(
        "screening__cancer_types__name"
    ).annotate(
        enrolled=Count("id")
    )

    # 3. Merge manually
    enrolled_map = {
        e["screening__cancer_types__name"]: e["enrolled"]
        for e in enrolled_data
    }

    cancer_progress = []
    for t in target_data:
        name = t["cancer_type__name"]
        cancer_progress.append({
            "cancer_type__name": name,
            "target": t["target"],
            "enrolled": enrolled_map.get(name, 0)
        })

    # =========================
    # 🔬 SITE × CANCER (FIXED)
    # =========================
    detailed_progress = targets.values(
        "site__name",
        "cancer_type__name",
        "target_enrollment"
    ).annotate(
        enrolled=Count(
            "cancer_type__screening_cancer__enrollment",
            distinct=True
        )
    )

    # =========================
    # PATIENT STATS
    # =========================
    patient_category_stats = enrollments.values(
        "pt_category__name"
    ).annotate(
        total=Count("id")
    ).order_by("pt_category__name")


    patient_type_stats = enrollments.values(
        "pt_type__name"
    ).annotate(
        total=Count("id")
    ).order_by("pt_type__name")


    patient_combined_stats = enrollments.values(
        "pt_category__name",
        "pt_type__name"
    ).annotate(
        total=Count("id")
    ).order_by("pt_category__name", "pt_type__name")

    # =========================
    # % HELPERS
    # =========================
    total_enrolled = enrolled_subjects

    def add_percentage(data, total):
        results = []
        for row in data:
            count = row.get("total", 0)
            percent = int((count / total) * 100) if total > 0 else 0
            row["percent"] = percent
            results.append(row)
        return results

    def add_percent(data, target_field):
        results = []
        for row in data:
            target = row.get(target_field, 0) or 0
            enrolled = row.get("enrolled", 0) or 0
            percent = int((enrolled / target) * 100) if target > 0 else 0
            row["percent"] = percent
            results.append(row)
        return results

    # Apply %
    site_progress = add_percent(site_progress, "target")
    cancer_progress = add_percent(cancer_progress, "target")
    detailed_progress = add_percent(detailed_progress, "target_enrollment")

    patient_category_stats = add_percentage(patient_category_stats, total_enrolled)
    patient_type_stats = add_percentage(patient_type_stats, total_enrolled)
    patient_combined_stats = add_percentage(patient_combined_stats, total_enrolled)  # ✅ FIXED

    # =========================
    # OTHER
    # =========================
    site_summary = subjects.values("site__name").annotate(
        total=Count("id")
    )

    latest_subjects = subjects.select_related("site").order_by("-created_at")[:10]

    # =========================
    # RESPONSE
    # =========================
    return render(request, "dashboard/dashboard.html", {
        "role": role,

        # KPI
        "total_subjects": total_subjects,
        "screened_subjects": screened_subjects,
        "enrolled_subjects": enrolled_subjects,

        # Visits
        "scheduled_visits": scheduled_visits,
        "completed_visits": completed_visits,
        "missed_visits": missed_visits,
        "overdue_visits": overdue_visits,

        # Safety
        "adverse_events": adverse_events,

        # Overall
        "total_target": total_target,
        "overall_percent": overall_percent,

        # Progress
        "site_progress": site_progress,
        "cancer_progress": cancer_progress,
        "detailed_progress": detailed_progress,

        # Patient
        "patient_category_stats": patient_category_stats,
        "patient_type_stats": patient_type_stats,
        "patient_combined_stats": patient_combined_stats,

        # Other
        "site_summary": site_summary,
        "latest_subjects": latest_subjects,
    })