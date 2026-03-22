# herbal/models/crfs/crf1_radiotherapy_model.py

from django.db import models
from choices.models import YesNoUnk
from .crf1_model import CRF1


class CRF1Radiotherapy(models.Model):
    crf = models.ForeignKey(CRF1, on_delete=models.CASCADE, related_name="radiotherapies")

    radiotherapy = models.CharField(max_length=255)
    radiotherapy_start = models.DateField()
    radiotherapy_ongoing = models.ForeignKey(YesNoUnk, on_delete=models.PROTECT)
    radiotherapy_end = models.DateField(null=True, blank=True)
    radiotherapy_dose = models.CharField(max_length=255)
    radiotherapy_frequency = models.CharField(max_length=255)
    radiotherapy_remarks = models.TextField(blank=True)
    
    def __str__(self):
        return self.radiotherapy