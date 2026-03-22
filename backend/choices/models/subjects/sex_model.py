# choices/models/sex_model.py

from django.db import models
from datetime import date

class Sex(models.Model):
    
    code = models.CharField(max_length=4)  
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name="Sex"
        verbose_name_plural="Sex"
        
    def __str__(self):
        # return f"{self.code} - {self.name}"
        return f"{self.name}"

