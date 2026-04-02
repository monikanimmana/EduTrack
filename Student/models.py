from django.db import models

class Department(models.Model):
    department = models.CharField(max_length=200)

    def __str__(self):
        return self.department

    class Meta:
        ordering = ['department']


class StudentID(models.Model):
    student_id = models.CharField(max_length=500)

    def __str__(self):
        return self.student_id


class Student(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    student_id = models.OneToOneField(StudentID, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=200)
    student_age = models.IntegerField(default=18)
    student_email = models.EmailField(unique=True)
    student_address = models.CharField(max_length=500)

    def __str__(self):
        return self.student_name

    class Meta:
        ordering = ['student_name']


class Subject(models.Model):
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.subject


class SubjectMarks(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="marks")
    marks = models.IntegerField()

    class Meta:
        unique_together = ('student', 'subject')