# choices/models/missed_visit_reason.py

from choices.models import BaseChoiceModel


class MissedVisitReason(BaseChoiceModel):

    class Meta:
        verbose_name = "Missed Visit Reason"
        verbose_name_plural = "Missed Visit Reasons"
