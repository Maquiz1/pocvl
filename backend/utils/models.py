from django.db import models

class EmailRecipient(models.Model):
    TYPE_CHOICES = [
        ("cc", "CC"),
        ("bcc", "BCC"),
    ]

    email = models.EmailField(unique=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type.upper()}: {self.email}"

    class Meta:
        ordering = ["type", "email"]
        
        
class SiteConfiguration(models.Model):
    name = models.CharField(max_length=100, unique=True)
    site_url = models.URLField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.site_url})"

    class Meta:
        ordering = ["name"]

