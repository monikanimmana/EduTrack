from django.db import models
from students.models import Student, Subject


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    exam_date = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'subject')
        ordering = ['subject__name']

    def __str__(self):
        return f"{self.student.student_id} - {self.subject.name}: {self.score}"

    @property
    def percentage(self):
        if self.max_score:
            return round((self.score / self.max_score) * 100, 2)
        return 0

    @property
    def grade(self):
        p = self.percentage
        if p >= 90: return 'A+'
        if p >= 80: return 'A'
        if p >= 70: return 'B'
        if p >= 60: return 'C'
        if p >= 50: return 'D'
        return 'F'
