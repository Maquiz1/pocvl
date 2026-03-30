# herbal/models/crfs/crf4_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule
from core.models import BaseModel
from choices.models import Grade,Appearance


class CRF4(BaseModel):

    visit = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="crf4"
    )

    # --- General ---
    sample_date = models.DateField()

    # --- Renal Function ---
    renal_urea = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    renal_urea_units = models.CharField(max_length=50, blank=True)
    renal_urea_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="renal_urea_grades")

    renal_creatinine = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    renal_creatinine_units = models.CharField(max_length=50, blank=True)
    renal_creatinine_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="renal_creatinine_grades")

    renal_egfr = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    renal_egfr_units = models.CharField(max_length=50, blank=True)
    renal_egfr_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="renal_egfr_grades")

    # --- Liver Function ---
    liver_ast = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    liver_ast_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="liver_ast_grades")

    liver_alt = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    liver_alt_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="liver_alt_grades")

    liver_alp = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    liver_alp_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="liver_alp_grades")

    liver_pt = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    liver_pt_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="liver_pt_grades")

    liver_ptt = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    liver_ptt_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="liver_ptt_grades")

    liver_inr = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    liver_inr_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="liver_inr_grades")

    liver_ggt = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    liver_ggt_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="liver_ggt_grades")

    liver_albumin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    liver_albumin_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="liver_albumin_grades")

    liver_bilirubin_total = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    liver_bilirubin_total_units = models.CharField(max_length=50, blank=True)
    bilirubin_total_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="bilirubin_total_grades")

    liver_bilirubin_direct = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    liver_bilirubin_direct_units = models.CharField(max_length=50, blank=True)
    bilirubin_direct_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="bilirubin_direct_grades")

    # --- Inflammation / Metabolic ---
    ldh = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    ldh_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="ldh_grades")

    crp = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    crp_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="crp_grades")

    d_dimer = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    d_dimer_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="d_dimer_grades")

    ferritin = models.DecimalField(max_digits=7, decimal_places=1, null=True, blank=True)
    ferritin_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="ferritin_grades")

    rbg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rbg_units = models.CharField(max_length=50, blank=True)
    rbg_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="rbg_grades")

    # --- Hematology ---
    hb = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hb_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="hb_grades")

    hct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hct_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="hct_grades")

    rbc = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rbc_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="rbc_grades")

    wbc = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    wbc_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="wbc_grades")

    plt = models.DecimalField(max_digits=7, decimal_places=0, null=True, blank=True)
    plt_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="plt_grades")

    abs_neutrophil = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    abs_neutrophil_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="abs_neutrophil_grades")

    abs_lymphocytes = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    abs_lymphocytes_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="abs_lymphocytes_grades")

    abs_eosinophils = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    abs_eosinophils_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="abs_eosinophils_grades")

    abs_monocytes = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    abs_monocytes_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="abs_monocytes_grades")

    abs_basophils = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    abs_basophils_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="abs_basophils_grades")

    mcv = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mcv_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="mcv_grades")

    mch = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mch_grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL, related_name="mch_grades")

    # --- Imaging / Cancer ---
    cancer = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    prostate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    chest_xray = models.ForeignKey(Appearance, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")
    chest_specify = models.TextField(blank=True)

    ct_chest = models.ForeignKey(Appearance, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")
    ct_chest_specify = models.TextField(blank=True)

    ultrasound = models.ForeignKey(Appearance, null=True, blank=True, on_delete=models.SET_NULL,related_name="+")
    ultrasound_specify = models.TextField(blank=True)

    remarks = models.TextField(blank=True)