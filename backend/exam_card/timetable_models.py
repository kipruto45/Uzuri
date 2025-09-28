from django.db import models
from core.models import Unit

class ExamTimetable(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    exam_date = models.DateField()
    exam_time = models.TimeField()
    exam_type = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.unit.code} {self.exam_type} {self.exam_date} {self.exam_time}"