# herbal/models/crfs/crf1_chemotherapy_model.py

from django.db import models
from choices.models import YesNoUnk
from .crf1_model import CRF1


class CRF1Chemotherapy(models.Model):
    crf = models.ForeignKey(CRF1, on_delete=models.CASCADE, related_name="chemotherapies")

    chemotherapy = models.CharField(max_length=255)
    chemotherapy_start = models.DateField()
    chemotherapy_ongoing = models.ForeignKey(YesNoUnk, on_delete=models.PROTECT)
    chemotherapy_end = models.DateField(null=True, blank=True)
    chemotherapy_dose = models.CharField(max_length=255)
    chemotherapy_frequency = models.CharField(max_length=255)
    chemotherapy_remarks = models.TextField(blank=True)
    
    def __str__(self):
        return self.chemotherapy