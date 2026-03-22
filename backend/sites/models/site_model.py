# sites/models/site_model.py

from choices.models import BaseChoiceModel

class Site(BaseChoiceModel):

    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Sites"
    
    def __str__(self):
        return f"{self.name} - {self.label}"

