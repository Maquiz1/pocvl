from django.utils import timezone


def update_visit_status(visit):

    # Do not modify if NA
    if visit.status == "na":
        return

    required_forms = ["crf2", "crf3", "crf4", "crf7"]

    if visit.visit_day == "D0":
        required_forms.append("crf1")

    filled = []
    missing = []

    for form in required_forms:
        if hasattr(visit, form):
            filled.append(form)
        else:
            missing.append(form)

    # ---------------- LOGIC ----------------

    # No CRFs + no visit date
    if not filled and not visit.actual_visit_date:
        visit.status = "pending"

    # At least one CRF → incomplete
    elif filled and missing:
        visit.status = "incomplete"

        # # auto set visit date if missing
        # if not visit.actual_visit_date:
        #     visit.actual_visit_date = timezone.now().date()

    # All CRFs done
    elif not missing:
        visit.status = "completed"

        if not visit.actual_visit_date:
            visit.actual_visit_date = visit.scheduled_date

    visit.save()