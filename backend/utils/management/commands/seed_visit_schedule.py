from django.core.management.base import BaseCommand
from herbal.models import VisitScheduleConfig
from choices.models import VisitDay


class Command(BaseCommand):
    help = "Seed default VisitScheduleConfig"

    def handle(self, *args, **kwargs):

        mapping = {
            "D0": 0,
            "D7": 7,
            "D14": 14,
            "D30": 30,
            "D60": 60,
            "D90": 90,
            "D120": 120,
        }

        created_count = 0

        for code, offset in mapping.items():
            try:
                visit_day = VisitDay.objects.get(code=code)

                obj, created = VisitScheduleConfig.objects.update_or_create(
                    visit_day=visit_day,
                    defaults={
                        "offset_days": offset,
                        "is_active": True,
                    }
                )

                if created:
                    created_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"{code} → {offset} days {'(created)' if created else '(updated)'}"
                    )
                )

            except VisitDay.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"❌ VisitDay {code} does not exist")
                )

        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Done. {created_count} configs created.")
        )