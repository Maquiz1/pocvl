# herbal/models/crfs/crf1_nimregenin_model.py

from django.db import models
from choices.models import YesNoUnk
from .crf1_model import CRF1
from django.core.validators import MaxValueValidator, MinValueValidator


class CRF1Nimregenin(models.Model):

    crf = models.ForeignKey(
        CRF1,
        on_delete=models.CASCADE,
        related_name="nimregenins"
    )

    nimregenin_preparation = models.CharField(max_length=255)

    nimregenin_start = models.DateField(null=True, blank=True)

    nimregenin_ongoing = models.ForeignKey(
        YesNoUnk,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    nimregenin_end = models.DateField(null=True, blank=True)

    nimregenin_dose = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    nimregenin_frequency = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(255)],
        null=True,
        blank=True
    )
    nimregenin_remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Nimregenin - {self.nimregenin_preparation}"