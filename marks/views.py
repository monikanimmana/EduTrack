from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Marks
from .serializers import MarksSerializer
from users.permissions import IsAdminOrTeacher, IsTeacherOrReadOnly
from students.models import Student


class MarksViewSet(viewsets.ModelViewSet):
    queryset = Marks.objects.select_related('student', 'subject').all()
    serializer_class = MarksSerializer
    permission_classes = [IsTeacherOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['student', 'subject']
    search_fields = ['student__student_id', 'subject__name']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_student():
            student = get_object_or_404(Student, user=user)
            return qs.filter(student=student)
        if user.is_teacher():
            try:
                subjects = user.teacher_profile.subjects.all()
                return qs.filter(subject__in=subjects)
            except Exception:
                return qs.none()
        return qs  # admin sees all


@login_required
def marks_view(request):
    user = request.user

    if user.is_admin():
        students = Student.objects.prefetch_related('marks__subject').all()
        return render(request, 'teacher/marks.html', {'students': students, 'is_admin': True})

    if user.is_teacher():
        try:
            my_subjects = user.teacher_profile.subjects.all()
        except Exception:
            my_subjects = []
        students = Student.objects.prefetch_related('marks__subject').all()
        # filter marks to only teacher's subjects
        for s in students:
            s.filtered_marks = s.marks.filter(subject__in=my_subjects)
        return render(request, 'teacher/marks.html', {
            'students': students,
            'my_subjects': my_subjects,
            'is_admin': False,
        })

    # Student
    student = get_object_or_404(Student, user=user)
    marks = Marks.objects.filter(student=student).select_related('subject')
    total = marks.aggregate(total=Sum('score'))['total'] or 0
    avg   = marks.aggregate(avg=Avg('score'))['avg'] or 0
    return render(request, 'student/marks.html', {
        'marks': marks, 'total': total, 'avg': round(avg, 2)
    })
