# herbal/models/crfs/crf1_other_herbal_model.py

from django.db import models
from choices.models import YesNoUnk
from .crf1_model import CRF1


class CRF1OtherHerbal(models.Model):

    crf = models.ForeignKey(
        CRF1,
        on_delete=models.CASCADE,
        related_name="other_herbals"
    )

    herbal_preparation = models.CharField(max_length=255)

    herbal_start = models.DateField()

    herbal_ongoing = models.ForeignKey(
        YesNoUnk,
        on_delete=models.PROTECT
    )

    herbal_end = models.DateField(null=True, blank=True)

    herbal_dose = models.CharField(max_length=255)

    herbal_frequency = models.CharField(max_length=255)

    herbal_remarks = models.TextField(blank=True)

    def __str__(self):
        return self.herbal_preparation