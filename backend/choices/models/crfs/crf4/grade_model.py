# choices/models/grade_model.py

from ...base_model import BaseChoiceModel

class Grade(BaseChoiceModel):

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        
# class Grade(models.Model):

    # GRADE_CHOICES = [
    #     ("0", "Grade 0 (Normal)"),
    #     ("1", "Grade 1 (Mild)"),
    #     ("2", "Grade 2 (Moderate)"),
    #     ("3", "Grade 3 (Severe)"),
    #     ("4", "Grade 4 (Life-threatening)"),
    # ]

    # name = models.CharField(max_length=10, choices=GRADE_CHOICES, unique=True)

    # description = models.CharField(max_length=255, blank=True)

    # def __str__(self):
    #     return self.get_name_display()