# choices/models/id_type_model.py

from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100)

class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Ward(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)