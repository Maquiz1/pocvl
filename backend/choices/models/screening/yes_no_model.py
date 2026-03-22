# choices/models/screening/yes_no_model.py

from django.db import models
from datetime import date

class YesNo(models.Model):
    value = models.IntegerField()  
    code = models.CharField(max_length=50)  
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name="YesNo"
        verbose_name_plural="YesNo"
        
    def __str__(self):
        # return f"{self.id} - {self.value} - {self.code} - {self.name}"
        return f"{self.name}"

