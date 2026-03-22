# herbal/models/cancers/cancer_type_model.py

from django.db import models

class CancerType(models.Model):

    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True)

    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Cancer Type"
        verbose_name_plural = "Cancer Types"

    def __str__(self):
        return f"{self.name} ({self.code})"