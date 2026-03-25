# herbal/models/crfs/crf2_other_model.py

from django.db import models
from .crf2_model import CRF2
from choices.models import YesNoUnk, Appearance


class CRF2OtherPhysclExam(models.Model):
    crf2 = models.ForeignKey(
        CRF2,
        on_delete=models.CASCADE,
        related_name="other_physcl_exams"
    )

    system = models.CharField(max_length=255, blank=True)

    finding = models.ForeignKey(
        Appearance,   # or your system list model
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    comments = models.TextField(null=True, blank=True)
    signifcnt = models.ForeignKey(
        YesNoUnk,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.crf2} - {self.system}"