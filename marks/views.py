from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Marks
from .serializers import MarksSerializer
from users.permissions import IsTeacher, IsTeacherOrReadOnly
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
        if self.request.user.is_student():
            student = get_object_or_404(Student, user=self.request.user)
            return qs.filter(student=student)
        return qs


# ── HTML Views ───────────────────────────────────────────────────────────────

@login_required
def marks_view(request):
    if request.user.is_teacher():
        students = Student.objects.prefetch_related('marks__subject').all()
        return render(request, 'teacher/marks.html', {'students': students})
    student = get_object_or_404(Student, user=request.user)
    marks = Marks.objects.filter(student=student).select_related('subject')
    total = marks.aggregate(total=Sum('score'))['total'] or 0
    avg = marks.aggregate(avg=Avg('score'))['avg'] or 0
    return render(request, 'student/marks.html', {'marks': marks, 'total': total, 'avg': round(avg, 2)})
