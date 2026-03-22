from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    value = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        # verbose_name = "Marital Status"
        # verbose_name_plural = "Marital Statuses"
        ordering = ['code']  # or ['code']
        indexes = [
            models.Index(fields=["name"]),
        ]
        
    def __str__(self):
        # return f"{self.code} - {self.name}"
        return f"{self.name}"

class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="districts", db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    value = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        # verbose_name = "Marital Status"
        # verbose_name_plural = "Marital Statuses"
        ordering = ['code']  # or ['code']
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["region", "name"]),  # 🔥 combo lookup
        ]
        
    def __str__(self):
        # return f"{self.code} - {self.name}"
        return f"{self.name}"


class Ward(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="wards", db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    value = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        # verbose_name = "Marital Status"
        # verbose_name_plural = "Marital Statuses"
        ordering = ['code']  # or ['code']
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["district", "name"]),  # 🔥 combo lookup
        ]
                
    def __str__(self):
        # return f"{self.code} - {self.name}"
        return f"{self.name}"


class Street(models.Model):
    ward = models.ForeignKey(
        Ward,
        on_delete=models.CASCADE,
        related_name="streets",
        db_index=True
    )
    name = models.CharField(max_length=150, db_index=True)
    code = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    value = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # verbose_name = "Marital Status"
        # verbose_name_plural = "Marital Statuses"
        unique_together = ("ward", "name")
        ordering = ['id']  # or ['code']
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["ward", "name"]),  # 🔥 combo lookup
        ]
        
    def __str__(self):
        # return f"{self.id} - {self.name}"
        return f"{self.name}"
