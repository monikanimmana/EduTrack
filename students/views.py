from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Department, Student, Subject
from .serializers import (
    DepartmentSerializer, StudentSerializer,
    StudentCreateSerializer, SubjectSerializer,
)
from users.permissions import IsTeacher, IsTeacherOrReadOnly


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsTeacherOrReadOnly]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsTeacherOrReadOnly]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user', 'department').all()
    permission_classes = [IsTeacher]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department']
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['student_id', 'enrolled_date']

    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        return StudentSerializer


# ── HTML Views ───────────────────────────────────────────────────────────────

@login_required
def student_list_view(request):
    if not request.user.is_teacher():
        return redirect('student_profile')
    students = Student.objects.select_related('user', 'department').all()
    search = request.GET.get('q', '')
    if search:
        students = students.filter(
            student_id__icontains=search
        ) | students.filter(user__first_name__icontains=search) | \
            students.filter(user__last_name__icontains=search)
    return render(request, 'teacher/students.html', {'students': students, 'search': search})


@login_required
def student_profile_view(request):
    if request.user.is_teacher():
        return redirect('student_list')
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'student/profile.html', {'student': student})
