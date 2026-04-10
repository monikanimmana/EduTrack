from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Fee
from .serializers import FeeSerializer
from users.permissions import IsTeacher, IsTeacherOrReadOnly
from students.models import Student


class FeeViewSet(viewsets.ModelViewSet):
    queryset = Fee.objects.select_related('student').all()
    serializer_class = FeeSerializer
    permission_classes = [IsTeacherOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'student']
    search_fields = ['student__student_id']

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_student():
            student = get_object_or_404(Student, user=self.request.user)
            return qs.filter(student=student)
        return qs


@login_required
def fees_view(request):
    if request.user.is_teacher():
        fees = Fee.objects.select_related('student__user').all()
        return render(request, 'teacher/fees.html', {'fees': fees})
    student = get_object_or_404(Student, user=request.user)
    fees = Fee.objects.filter(student=student)
    return render(request, 'student/fees.html', {'fees': fees})
