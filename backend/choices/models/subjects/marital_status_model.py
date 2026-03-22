# choices/models/marital_status_model.py

from django.db import models


class MaritalStatus(models.Model):
    
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Marital Status"
        verbose_name_plural = "Marital Statuses"
        ordering = ['id']  # or ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"