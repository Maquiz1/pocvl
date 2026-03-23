from django.db import models
from ...visits.visit_schedule_model import VisitSchedule
from core.models import BaseModel
from choices.models import YesNo, YesNoNa, YesNoUnk, Method,Appearance
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# from accounts.models import StaffProfile  # adjust path if needed


class CRF2(BaseModel):

    visit = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="crf2"
    )

    test_date = models.DateField()

    # =========================
    # VITALS (CLINICAL RANGES)
    # =========================

    # Height in cm (adult realistic range)
    height = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[
            MinValueValidator(50, message="Height too low (min 50 cm)"),
            MaxValueValidator(250, message="Height too high (max 250 cm)")
        ],
        null=True,
        blank=True
    )

    # Weight in kg
    weight = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[
            MinValueValidator(2, message="Weight too low"),
            MaxValueValidator(300, message="Weight too high")
        ],
        null=True,
        blank=True
    )

    # BMI (WHO realistic range)
    bmi = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(10, message="BMI too low"),
            MaxValueValidator(80, message="BMI too high")
        ],
        null=True,
        blank=True
    )
    
    vital_time = models.TimeField(null=True, blank=True)

    # TEMPRATURE
    temperature = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(28, message="Temperature too low"),
            MaxValueValidator(40, message="Temperature too high")
        ],
        null=True,
        blank=True
    )

    method = models.ForeignKey(Method, on_delete=models.SET_NULL, null=True, blank=True)

    # Respiratory rate (breaths/min)
    respiratory_rate = models.IntegerField(
        validators=[
            MinValueValidator(5),
            MaxValueValidator(60)
        ],
        null=True,
        blank=True
    )

    # Heart rate (bpm)
    heart_rate = models.IntegerField(
        validators=[
            MinValueValidator(30),
            MaxValueValidator(220)
        ],
        null=True,
        blank=True
    )

    # Blood pressure
    systolic = models.IntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(250)],
        null=True,
        blank=True
    )

    diastolic = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(150)],
        null=True,
        blank=True
    )

    phys_exm_time = models.TimeField(null=True, blank=True)

    # =========================
    # SYSTEM EXAMS
    # =========================
    def yn_field():
        return models.ForeignKey(
            YesNoUnk,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="+"
        )

    def appearance_field():
        return models.ForeignKey(
            Appearance,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="+"
        )

    appearance = appearance_field()
    appearance_comments = models.TextField(blank=True)
    appearance_signifcnt = yn_field()

    heent = appearance_field()
    heent_comments = models.TextField(blank=True)
    heent_signifcnt = yn_field()

    respiratory = appearance_field()
    respiratory_comments = models.TextField(blank=True)
    respiratory_signifcnt = yn_field()

    cardiovascular = appearance_field()
    cardiovascular_comments = models.TextField(blank=True)
    cardiovascular_signifcnt = yn_field()

    abdominal = appearance_field()
    abdominal_comments = models.TextField(blank=True)
    abdominal_signifcnt = yn_field()

    urogenital = appearance_field()
    urogenital_comments = models.TextField(blank=True)
    urogenital_signifcnt = yn_field()

    musculoskeletal = appearance_field()
    musculoskeletal_comments = models.TextField(blank=True)
    musculoskeletal_signifcnt = yn_field()

    neurological = appearance_field()
    neurological_comments = models.TextField(blank=True)
    neurological_signifcnt = yn_field()

    psychological = appearance_field()
    psychological_comments = models.TextField(blank=True)
    psychological_signifcnt = yn_field()

    endocrine = appearance_field()
    endocrine_comments = models.TextField(blank=True)
    endocrine_signifcnt = yn_field()

    lymphatic = appearance_field()
    lymphatic_comments = models.TextField(blank=True)
    lymphatic_signifcnt = yn_field()

    skin = appearance_field()
    skin_comments = models.TextField(blank=True)
    skin_signifcnt = yn_field()

    local_examination = appearance_field()
    local_examination_comments = models.TextField(blank=True)
    local_examination_signifcnt = yn_field()

    # =========================
    # OTHER EXAMS
    # =========================
    physical_exams_other = yn_field()
    physical_other_specify = models.CharField(max_length=255, blank=True)
    physical_other_system = appearance_field()
    physical_other_comments = models.TextField(blank=True)
    physical_other_signifcnt = yn_field()

    # =========================
    # FINAL
    # =========================
    additional_notes = models.TextField(blank=True)


    physcl_pfmd_by = models.ForeignKey(
        "accounts.StaffProfile",   # 🔥 string reference (NO import)
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'site__isnull': False}  # basic safety
    )
    
    date_completed = models.DateField(null=True,blank=True)

    remarks = models.TextField(blank=True)

    # =========================
    # 🔥 AUTO BMI CALCULATION
    # =========================
    def calculate_bmi(self):
        if self.height and self.weight:
            height_m = float(self.height) / 100  # cm → meters
            return round(float(self.weight) / (height_m ** 2), 2)
        return None

    # =========================
    # 🔥 VALIDATION
    # =========================
    def clean(self):
        super().clean()

        # Auto-calculate BMI
        if self.height and self.weight:
            calculated_bmi = self.calculate_bmi()

            # If BMI exists, validate it
            if self.bmi:
                if abs(float(self.bmi) - calculated_bmi) > 0.5:
                    raise ValidationError({
                        "bmi": f"BMI incorrect. Expected approx {calculated_bmi}"
                    })
            else:
                self.bmi = calculated_bmi

        # Logical BP validation
        if self.systolic and self.diastolic:
            if self.systolic <= self.diastolic:
                raise ValidationError({
                    "systolic": "Systolic must be greater than diastolic"
                })

    # =========================
    # SAVE OVERRIDE
    # =========================
    def save(self, *args, **kwargs):
        self.full_clean()  # enforce validation + BMI calc
        super().save(*args, **kwargs)

    def __str__(self):
        return f"CRF2 Visit {self.visit_id}"