# choices/models/enrollments/patient_category_model.py

from ..base_model import BaseChoiceModel

class PatientCategory(BaseChoiceModel):

    class Meta:
        verbose_name = "Patient Category"
        verbose_name_plural = "Patient Categories"

