# herbal/models/crfs/crf1_radiotherapy_model.py

from django.db import models
from choices.models import YesNoUnk
from .crf1_model import CRF1
from django.core.validators import MaxValueValidator, MinValueValidator


class CRF1Radiotherapy(models.Model):
    crf = models.ForeignKey(CRF1, on_delete=models.CASCADE, related_name="radiotherapies")

    radiotherapy = models.CharField(max_length=255)
    radiotherapy_start = models.DateField()
    radiotherapy_ongoing = models.ForeignKey(YesNoUnk, on_delete=models.PROTECT)
    radiotherapy_end = models.DateField(null=True, blank=True)
    radiotherapy_dose = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    radiotherapy_frequency = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(255)],
        null=True,
        blank=True
    )
    radiotherapy_remarks = models.TextField(blank=True)
    
    def __str__(self):
        return self.radiotherapy