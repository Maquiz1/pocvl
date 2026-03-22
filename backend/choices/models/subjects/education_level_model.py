# choices/models/education_level_model.py

from django.db import models


class EducationLevel(models.Model):
    
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Education Level"
        verbose_name_plural = "Education Levels"
        ordering = ['id']

    def __str__(self):
        return f"{self.code} - {self.name}"