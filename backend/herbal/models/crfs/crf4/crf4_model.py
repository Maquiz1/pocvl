# herbal/models/crfs/crf4_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule
from core.models import BaseModel



class CRF4(BaseModel):

    visit = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="crf4"
    )
    
    # --- General ---
    sample_date = models.DateField()

    # --- Renal Function ---
    renal_urea = models.FloatField(null=True, blank=True)
    renal_urea_units = models.CharField(max_length=50, blank=True)

    renal_creatinine = models.FloatField(null=True, blank=True)
    renal_creatinine_units = models.CharField(max_length=50, blank=True)
    renal_creatinine_grade = models.CharField(max_length=50, blank=True)

    renal_egfr = models.FloatField(null=True, blank=True)
    renal_egfr_units = models.CharField(max_length=50, blank=True)
    renal_egfr_grade = models.CharField(max_length=50, blank=True)

    # --- Liver Function ---
    liver_ast = models.FloatField(null=True, blank=True)
    liver_ast_grade = models.CharField(max_length=50, blank=True)

    liver_alt = models.FloatField(null=True, blank=True)
    liver_alt_grade = models.CharField(max_length=50, blank=True)

    liver_alp = models.FloatField(null=True, blank=True)
    liver_alp_grade = models.CharField(max_length=50, blank=True)

    liver_pt = models.FloatField(null=True, blank=True)
    liver_pt_grade = models.CharField(max_length=50, blank=True)

    liver_ptt = models.FloatField(null=True, blank=True)
    liver_ptt_grade = models.CharField(max_length=50, blank=True)

    liver_inr = models.FloatField(null=True, blank=True)
    liver_inr_grade = models.CharField(max_length=50, blank=True)

    liver_ggt = models.FloatField(null=True, blank=True)

    liver_albumin = models.FloatField(null=True, blank=True)
    liver_albumin_grade = models.CharField(max_length=50, blank=True)

    liver_bilirubin_total = models.FloatField(null=True, blank=True)
    liver_bilirubin_total_units = models.CharField(max_length=50, blank=True)
    bilirubin_total_grade = models.CharField(max_length=50, blank=True)

    liver_bilirubin_direct = models.FloatField(null=True, blank=True)
    liver_bilirubin_direct_units = models.CharField(max_length=50, blank=True)
    bilirubin_direct_grade = models.CharField(max_length=50, blank=True)

    # --- Glucose / Inflammation ---
    rbg = models.FloatField(null=True, blank=True)
    rbg_units = models.CharField(max_length=50, blank=True)
    rbg_grade = models.CharField(max_length=50, blank=True)

    ldh = models.FloatField(null=True, blank=True)
    crp = models.FloatField(null=True, blank=True)
    d_dimer = models.FloatField(null=True, blank=True)
    ferritin = models.FloatField(null=True, blank=True)

    # --- Hematology ---
    wbc = models.FloatField(null=True, blank=True)
    wbc_grade = models.CharField(max_length=50, blank=True)

    abs_neutrophil = models.FloatField(null=True, blank=True)
    abs_neutrophil_grade = models.CharField(max_length=50, blank=True)

    abs_lymphocytes = models.FloatField(null=True, blank=True)
    abs_lymphocytes_grade = models.CharField(max_length=50, blank=True)

    abs_eosinophils = models.FloatField(null=True, blank=True)
    abs_monocytes = models.FloatField(null=True, blank=True)
    abs_basophils = models.FloatField(null=True, blank=True)

    hb = models.FloatField(null=True, blank=True)
    hb_grade = models.CharField(max_length=50, blank=True)

    mcv = models.FloatField(null=True, blank=True)
    mch = models.FloatField(null=True, blank=True)
    hct = models.FloatField(null=True, blank=True)
    rbc = models.FloatField(null=True, blank=True)

    plt = models.FloatField(null=True, blank=True)
    plt_grade = models.CharField(max_length=50, blank=True)

    # --- Imaging / Cancer ---
    cancer = models.BooleanField(default=False)
    prostate = models.BooleanField(default=False)

    chest_xray = models.BooleanField(default=False)
    chest_specify = models.TextField(blank=True)

    ct_chest = models.BooleanField(default=False)
    ct_chest_specify = models.TextField(blank=True)

    ultrasound = models.BooleanField(default=False)
    ultrasound_specify = models.TextField(blank=True)
    
    remarks = models.TextField(blank=True)

