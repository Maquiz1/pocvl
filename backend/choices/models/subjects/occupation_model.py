# choices/models/occupation_model.py

from ..base_model import BaseChoiceModel


class Occupation(BaseChoiceModel):

    class Meta:
        verbose_name = "Occupation"
        verbose_name_plural = "Occupations"
