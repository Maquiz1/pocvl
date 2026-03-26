from datetime import timedelta
from herbal.models import VisitSchedule
from herbal.models import VisitScheduleConfig
import traceback


def generate_visit_schedule(enrollment):
    print("🔥 SCHEDULER TRIGGERED", enrollment.id)

    enrollment_date = enrollment.enrollment_date

    configs = VisitScheduleConfig.objects.select_related("visit_day") \
        .filter(is_active=True) \
        .order_by("visit_day__order")

    print("CONFIG COUNT:", configs.count())  # 👈 ADD THIS

    for config in configs:

        scheduled_date = enrollment_date + timedelta(days=config.offset_days)

        visit, created = VisitSchedule.objects.get_or_create(
            enrollment=enrollment,
            visit_day=config.visit_day,
            defaults={"scheduled_date": scheduled_date},
        )

        if not created and visit.scheduled_date != scheduled_date:
            visit.scheduled_date = scheduled_date
            visit.save(update_fields=["scheduled_date"])
            
            
            
def update_visit_schedule(enrollment):
    print("🧠 SMART UPDATE", enrollment.id)

    from datetime import timedelta
    from herbal.models import VisitScheduleConfig

    enrollment_date = enrollment.enrollment_date

    configs = VisitScheduleConfig.objects.filter(is_active=True)

    for config in configs:

        new_date = enrollment_date + timedelta(days=config.offset_days)

        try:
            visit = enrollment.visits.get(visit_day=config.visit_day)

            # ✅ DO NOT change completed visits
            if visit.status == "completed":
                continue

            # ✅ Only update if changed
            if visit.scheduled_date != new_date:
                visit.scheduled_date = new_date
                visit.save(update_fields=["scheduled_date"])
                print(f"✏️ Updated {config.visit_day.code}")

        except VisitSchedule.DoesNotExist:
            # ✅ Create missing visit
            VisitSchedule.objects.create(
                enrollment=enrollment,
                visit_day=config.visit_day,
                scheduled_date=new_date
            )
            print(f"➕ Created {config.visit_day.code}")