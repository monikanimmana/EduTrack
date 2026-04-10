import uuid
from django.db import models
from django.utils import timezone
from students.models import Student, Subject


class Session(models.Model):
    """A class/lecture session for which attendance is tracked."""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    qr_valid_until = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        'users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='sessions_created'
    )

    def __str__(self):
        return f"{self.subject.name} - {self.date}"

    def is_qr_valid(self):
        if not self.qr_valid_until:
            return False
        return timezone.now() <= self.qr_valid_until

    class Meta:
        ordering = ['-date', '-start_time']


class Attendance(models.Model):
    METHOD_MANUAL = 'manual'
    METHOD_QR = 'qr'
    METHOD_CHOICES = [
        (METHOD_MANUAL, 'Manual'),
        (METHOD_QR, 'QR Code'),
    ]

    STATUS_PRESENT = 'present'
    STATUS_ABSENT = 'absent'
    STATUS_LATE = 'late'
    STATUS_CHOICES = [
        (STATUS_PRESENT, 'Present'),
        (STATUS_ABSENT, 'Absent'),
        (STATUS_LATE, 'Late'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PRESENT)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default=METHOD_MANUAL)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'student')
        ordering = ['-marked_at']

    def __str__(self):
        return f"{self.student.student_id} - {self.session} - {self.status}"
