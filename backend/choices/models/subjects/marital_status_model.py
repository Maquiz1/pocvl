# choices/models/marital_status_model.py

from ..base_model import BaseChoiceModel


class MaritalStatus(BaseChoiceModel):

    class Meta:
        verbose_name = "Marital Status"
        verbose_name_plural = "Marital Statuses"
