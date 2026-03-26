from django.core.management.base import BaseCommand
from herbal.models import VisitSchedule
from choices.models import MissedVisitReason


class Command(BaseCommand):
    help = "Migrate missed_reason (char) → missed_reason_fk (FK)"

    def handle(self, *args, **kwargs):

        self.stdout.write("🚀 Starting migration...")

        # preload for speed
        reason_map = {r.code: r for r in MissedVisitReason.objects.all()}

        updated = 0
        skipped = 0
        unknown = set()

        visits = VisitSchedule.objects.all()

        for visit in visits:

            old_reason = visit.missed_reason

            if not old_reason:
                skipped += 1
                continue

            reason_obj = reason_map.get(old_reason)

            if not reason_obj:
                unknown.add(old_reason)
                continue

            visit.missed_reason_fk = reason_obj
            visit.save(update_fields=["missed_reason_fk"])
            updated += 1

        # summary
        self.stdout.write(self.style.SUCCESS(f"✅ Updated: {updated}"))
        self.stdout.write(f"⏭ Skipped (no reason): {skipped}")

        if unknown:
            self.stdout.write(self.style.WARNING("⚠️ Unknown reasons found:"))
            for r in unknown:
                self.stdout.write(f" - {r}")

        self.stdout.write(self.style.SUCCESS("🎉 Migration complete"))