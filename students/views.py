from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Department, Student, Subject, TeacherProfile
from .serializers import (
    DepartmentSerializer, StudentSerializer,
    StudentCreateSerializer, SubjectSerializer,
)
from users.permissions import IsTeacher, IsTeacherOrReadOnly, IsAdmin


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
    if not request.user.is_student():
        return redirect('student_list')
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'student/profile.html', {'student': student})


@login_required
def teacher_list_view(request):
    if not request.user.is_admin():
        return redirect('dashboard')
    teachers = TeacherProfile.objects.select_related('user', 'department').prefetch_related('subjects').all()
    subjects = Subject.objects.all()
    departments = Department.objects.all()
    return render(request, 'admin/teachers.html', {
        'teachers': teachers,
        'subjects': subjects,
        'departments': departments,
    })


@login_required
def add_teacher_view(request):
    if not request.user.is_admin():
        return redirect('dashboard')
    if request.method == 'POST':
        from users.models import CustomUser
        username    = request.POST.get('username')
        first_name  = request.POST.get('first_name')
        last_name   = request.POST.get('last_name')
        email       = request.POST.get('email')
        password    = request.POST.get('password')
        subject_ids = request.POST.getlist('subjects')
        dept_id     = request.POST.get('department')
        phone       = request.POST.get('phone', '')
        qualification = request.POST.get('qualification', '')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('teacher_list')

        user = CustomUser.objects.create_user(
            username=username, email=email,
            first_name=first_name, last_name=last_name,
            password=password, role=CustomUser.ROLE_TEACHER
        )
        dept = Department.objects.filter(id=dept_id).first()
        profile = TeacherProfile.objects.create(user=user, department=dept, phone=phone, qualification=qualification)
        if subject_ids:
            profile.subjects.set(Subject.objects.filter(id__in=subject_ids))
        messages.success(request, f'Teacher {username} created successfully.')
        return redirect('teacher_list')
    return redirect('teacher_list')
