# herbal/models/crfs/crf6_model.py

from django.db import models
from ...enrollments.enrollment_model import Enrollment
from core.models import BaseModel
from choices.models import YesNoUnk

class CRF6(BaseModel):

    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="termination"
    )

    today_date = models.DateField(null=True, blank=True)

    termination_date = models.DateField(null=True, blank=True)
    completed120days = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")
    reported_dead = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")
    withdrew_consent = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    date_death = models.DateField(null=True, blank=True)
    primary_cause = models.CharField(max_length=255, blank=True)
    secondary_cause = models.CharField(max_length=255, blank=True)
    
    withdrew_reason = models.CharField(max_length=255, blank=True)
    
    withdrew_other = models.TextField(blank=True)
    
    
    outcome = models.CharField(max_length=255, blank=True)
    outcome_date = models.DateField(null=True, blank=True)
    
    summary = models.TextField(blank=True)
    clinician_name = models.CharField(max_length=255)
    
    
    remarks = models.TextField(blank=True)





    reason = models.CharField(
        max_length=50,
        choices=[
            ("completed","Completed Study"),
            ("ltf","Lost To Follow Up"),
            ("withdrawn","Participant Withdrew"),
            ("transfer_out","Transferred Out"),
            ("medical_reason","Medical Reason"),
        ]
    )

    terminated_reason = models.CharField(max_length=255, blank=True)
