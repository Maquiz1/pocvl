# choices/models/education_level_model.py

from ..base_model import BaseChoiceModel


class EducationLevel(BaseChoiceModel):

    class Meta:
        verbose_name = "Education Level"
        verbose_name_plural = "Education Levels"
