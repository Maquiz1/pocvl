# herbal/models/crfs/crf7_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule
from core.models import BaseModel
from choices.models import YesNo, YesNoNa, YesNoUnk

class CRF7(BaseModel):

    visit = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="crf7"
    )

    tdate = models.DateField(null=True, blank=True)
    fdate = models.DateField(null=True, blank=True)
    cdate = models.DateField(null=True, blank=True)

    cpersid = models.CharField(
        max_length=150,
        blank=True,
        help_text="Name of person entering data"
    )

    # ✅ FK fields (not integers)
    mobility = models.ForeignKey(
        YesNoUnk, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    self_care = models.ForeignKey(
        YesNoUnk, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    usual_active = models.ForeignKey(
        YesNoUnk, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    pain = models.ForeignKey(
        YesNoUnk, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    anxiety = models.ForeignKey(
        YesNoUnk, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    remarks = models.TextField(blank=True)
