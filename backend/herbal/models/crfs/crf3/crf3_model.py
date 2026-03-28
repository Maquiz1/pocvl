# herbal/models/crfs/crf3_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule
from core.models import BaseModel
from choices.models import YesNo, YesNoNa, YesNoUnk, Method,Appearance
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# from accounts.models import StaffProfile  # adjust path if needed


class CRF3(BaseModel):

    visit = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="crf3"
    )

    # Symptoms (FK to YesNoUnk)
    fever = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="fever_crf3")
    vomiting = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="vomiting_crf3")
    diarrhoea = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="diarrhoea_crf3")
    nausea = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="nausea_crf3")
    loss_appetite = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="loss_appetite_crf3")
    headaches = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="headaches_crf3")
    difficult_breathing = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="breathing_crf3")
    sore_throat = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="sore_throat_crf3")
    fatigue = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="fatigue_crf3")
    muscle_pain = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="muscle_pain_crf3")
    loss_consciousness = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="loss_consciousness_crf3")
    backpain = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="backpain_crf3")
    weight_loss = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="weight_loss_crf3")
    heartburn_indigestion = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="heartburn_crf3")
    swelling = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="swelling_crf3")
    pv_bleeding = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="pv_bleeding_crf3")
    pv_discharge = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="pv_discharge_crf3")
    micturition = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="micturition_crf3")
    convulsions = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="convulsions_crf3")
    blood_urine = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="blood_urine_crf3")

    # Other symptoms
    symptoms_other = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="symptoms_other_crf3")
    symptoms_other_specify = models.CharField(max_length=255, blank=True)

    # Adherence
    adherence = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="adherence_crf3")
    adherence_specify = models.CharField(max_length=255, blank=True)

    # Herbal medication
    herbal_medication = models.ForeignKey(YesNoUnk, null=True, blank=True, on_delete=models.SET_NULL, related_name="herbal_medication_crf3")
    herbal_ingredients = models.TextField(blank=True)
    
    remarks = models.TextField(blank=True)