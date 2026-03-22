# choices/models/id_type_model.py

from django.db import models


class IDType(models.Model):
    value = models.CharField(max_length=20, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "ID Type"
        verbose_name_plural = "ID Types"
        ordering = ['id']  # or ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"