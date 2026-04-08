from django.db import models
from django.conf import settings
from herbal.models import Site
from core.models import BaseModel
from choices.models import BaseChoiceModel

ROLE_CHOICES = [
    ("admin", "Admin"),
    ("data_manager", "Data Manager"),
    ("monitor", "Monitor"),
    ("coordinator", "Coordinator"),
    ("data_clerk", "Data Clerk"),
    ("reviewer", "Reviewer"),
    ("pi", "Principal Investigator"),
]

class Prefix(BaseChoiceModel):
    # name = models.CharField(max_length=20, unique=True)  
    # e.g. Dr., Mr., Ms., Prof., Nurse

    def __str__(self):
        return f"{self.id} - {self.code} - {self.name}"


class Position(BaseChoiceModel):
    # name = models.CharField(max_length=100, unique=True)  
    # e.g. Cardiologist, Study Coordinator, Nurse

    def __str__(self):
        return f"{self.id} - {self.code} - {self.name}"

class StaffProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="site_staff"
    )

    middle_name = models.CharField(
        max_length=150,
        blank=True
    )
    # ✅ NEW RELATIONS
    prefix = models.ForeignKey(
        Prefix,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
        
    assigned_sites = models.ManyToManyField(
        Site,
        blank=True,
        related_name="assigned_staff"
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    @property
    def full_name(self):
        first = self.user.first_name or ""
        middle = self.middle_name or ""
        last = self.user.last_name or ""

        # join safely (avoids extra spaces)
        return " ".join(part for part in [first, middle, last] if part).strip()

    @property
    def display_name(self):
        name = self.full_name

        if not name:
            name = self.user.email  # ✅ FIX (no username in your system)

        if self.prefix:
            name = f"{self.prefix.name} {name}"

        if self.position:
            name = f"{name} ({self.position.name})"

        return name
    
    def __str__(self):
        return f"{self.display_name}"
    
    
    
# # users/models.py
# from django.db import models
# from django.contrib.auth import get_user_model
# from phonenumber_field.modelfields import PhoneNumberField
# from locations.models import Site   # assuming this already exists

# User = get_user_model()

# class Prefix(models.Model):
#     name = models.CharField(max_length=10, unique=True)  # e.g., Dr, PhD, Prof
#     def __str__(self):
#         return self.name

# class Position(models.Model):
#     name = models.CharField(max_length=50, unique=True)  # e.g., Researcher, Clinician
#     def __str__(self):
#         return self.name

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)
#     phone_number = PhoneNumberField(null=True, blank=True, unique=True)
#     prefix = models.ForeignKey(Prefix, on_delete=models.SET_NULL, null=True, blank=True)
#     position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)

#     # NEW FIELDS
#     middle_name = models.CharField(max_length=50, blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
    
#     def __str__(self):
#         display_name = f"{self.prefix.name + ' ' if self.prefix else ''}{self.user.username}"
#         return f"{display_name} - {self.position.name if self.position else 'No Position'}"