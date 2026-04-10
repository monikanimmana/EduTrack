from django.db import models
from students.models import Student


class Fee(models.Model):
    STATUS_PAID = 'paid'
    STATUS_UNPAID = 'unpaid'
    STATUS_PARTIAL = 'partial'
    STATUS_CHOICES = [
        (STATUS_PAID, 'Paid'),
        (STATUS_UNPAID, 'Unpaid'),
        (STATUS_PARTIAL, 'Partial'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_UNPAID)
    due_date = models.DateField()
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.student_id} - {self.description} ({self.status})"

    def save(self, *args, **kwargs):
        if self.paid_amount >= self.amount:
            self.status = self.STATUS_PAID
        elif self.paid_amount > 0:
            self.status = self.STATUS_PARTIAL
        else:
            self.status = self.STATUS_UNPAID
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-due_date']
