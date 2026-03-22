# choices/models/id_type_model.py

from django.db import models
from ..base_model import BaseChoiceModel

class Region(BaseChoiceModel):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"

class District(BaseChoiceModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"
        
class Ward(BaseChoiceModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ward"
        verbose_name_plural = "Wards"
