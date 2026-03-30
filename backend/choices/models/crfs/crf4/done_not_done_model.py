# choices/models/grade_model.py

from ...base_model import BaseChoiceModel

class DoneNotDone(BaseChoiceModel):

    class Meta:
        verbose_name = "DoneNotDone"
        verbose_name_plural = "DoneNotDones"