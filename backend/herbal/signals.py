# herbal/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Enrollment
from .services.visit_scheduler import generate_visit_schedule,update_visit_schedule


@receiver(post_save, sender=Enrollment)
def create_visit_schedule(sender, instance, created, **kwargs):

    if created:
        generate_visit_schedule(instance)
    else:
        update_visit_schedule(instance)  # 👈 NEW
