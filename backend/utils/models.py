from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import timedelta
import logging
from django.utils import timezone

User = get_user_model()
logger = logging.getLogger(__name__)


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
        
        
        


class EmailLog(models.Model):

    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    error_message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    task_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_failed(self):
        return self.status == "failed"

    def __str__(self):
        return f"{self.subject} → {self.recipient} ({self.status})"

