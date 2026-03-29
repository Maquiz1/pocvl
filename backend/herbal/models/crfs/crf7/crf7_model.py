# herbal/models/crfs/crf7_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule
from core.models import BaseModel
from choices.models import Anxiety,Mobility,SelfCare, Pain, UsualActive

class CRF7(BaseModel):

    visit = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="crf7"
    )

    tdate = models.DateField(null=True, blank=True)
    fdate = models.DateField(null=True, blank=True)
    cdate = models.DateField(null=True, blank=True)

    cpersid = models.ForeignKey(
        "accounts.StaffProfile",   # 🔥 string reference (NO import)
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'site__isnull': False},  # basic safety
    )
    
    # ✅ FK fields (not integers)
    mobility = models.ForeignKey(
        Mobility, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    self_care = models.ForeignKey(
        SelfCare, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    usual_active = models.ForeignKey(
        UsualActive, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    pain = models.ForeignKey(
        Pain, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    anxiety = models.ForeignKey(
        Anxiety, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    remarks = models.TextField(blank=True)
    remarks2 = models.TextField(blank=True)
