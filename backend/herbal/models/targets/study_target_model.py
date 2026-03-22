# herbal/models/study_target_model.py

from django.db import models
from sites.models import Site
from herbal.models import CancerType


class StudyTarget(models.Model):

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    cancer_type = models.ForeignKey(CancerType, on_delete=models.CASCADE)

    target_enrollment = models.PositiveIntegerField()

    class Meta:
        unique_together = ("site", "cancer_type")

    def __str__(self):
        return f"{self.site} - {self.cancer_type} ({self.target_enrollment})"