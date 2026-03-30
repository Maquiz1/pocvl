# herbal/models/crfs/crf5_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule
from ...enrollments.enrollment_model import Enrollment
from core.models import BaseModel
from choices.models import YesNoUnk,AeCategory,AeActionTaken,AeOutcome,AeRelationship,AeSeverity,AeTreatment

class CRF5(BaseModel):

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="adverse_events"
    )

    date_reported = models.DateField(
        blank=True,
        null=True
    )
    
    # 🔥 THIS IS WHERE IT GOES
    after_visit = models.ForeignKey(
        VisitSchedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="adverse_after"
    )

    ae_description = models.TextField()
    
    ae_category = models.ForeignKey(AeCategory, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")


    ae_start_date = models.DateField(
        blank=True,
        null=True
    )

    ae_ongoing = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")

    ae_end_date = models.DateField(
        blank=True,
        null=True
    )

    ae_outcome = models.ForeignKey(AeOutcome, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")
    ae_severity = models.ForeignKey(AeSeverity, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")
    ae_serious = models.ForeignKey(AeSeverity, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")
    ae_expected = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")


    ae_treatment = models.ForeignKey(AeTreatment, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")
    ae_action_taken = models.ForeignKey(AeActionTaken, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")
    ae_relationship = models.ForeignKey(AeRelationship, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")

    ae_staff = models.ForeignKey(
        "accounts.StaffProfile",   # 🔥 string reference (NO import)
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'site__isnull': False},  # basic safety
    )
    
    ae_date = models.DateField(
        blank=True,
        null=True
    )
    
    remarks = models.TextField(blank=True)
