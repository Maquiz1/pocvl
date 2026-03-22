# herbal/models/crfs/crf1_surgery_model.py

from django.db import models
from choices.models import YesNoUnk
from .crf1_model import CRF1


class CRF1Surgery(models.Model):
    crf = models.ForeignKey(CRF1, on_delete=models.CASCADE, related_name="surgeries")

    surgery = models.CharField(max_length=255)
    surgery_start = models.DateField()
    surgery_number = models.IntegerField()
    surgery_remarks = models.TextField(blank=True)
    
    def __str__(self):
        return self.surgery