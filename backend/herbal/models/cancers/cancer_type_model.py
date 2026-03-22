# herbal/models/cancers/cancer_type_model.py

from choices.models import BaseChoiceModel

class CancerType(BaseChoiceModel):

    class Meta:
        verbose_name = "Cancer Type"
        verbose_name_plural = "Cancer Types"