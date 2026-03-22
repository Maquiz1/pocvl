# choices/models/occupation_model.py

from django.db import models


class Occupation(models.Model):
    value = models.CharField(max_length=20, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Occupation"
        verbose_name_plural = "Occupations"
        ordering = ['id']

    def __str__(self):
        return self.name