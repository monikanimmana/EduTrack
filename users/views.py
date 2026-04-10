from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from .permissions import IsAdmin


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class MeView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ── HTML Views ──────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials ❌')
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    user = request.user

    if user.is_admin():
        from students.models import Student, Department, TeacherProfile
        from marks.models import Marks
        from fees.models import Fee
        from attendance.models import Attendance, Session
        from django.utils import timezone

        context = {
            'total_students':  Student.objects.count(),
            'total_teachers':  TeacherProfile.objects.count(),
            'total_depts':     Department.objects.count(),
            'unpaid_fees':     Fee.objects.filter(status='unpaid').count(),
            'present_today':   Attendance.objects.filter(session__date=timezone.now().date(), status='present').count(),
            'active_sessions': Session.objects.filter(is_active=True).count(),
            'teachers':        TeacherProfile.objects.select_related('user').prefetch_related('subjects')[:5],
        }
        return render(request, 'admin/dashboard.html', context)

    if user.is_teacher():
        from students.models import TeacherProfile, Student
        from marks.models import Marks
        from attendance.models import Session, Attendance
        from django.utils import timezone

        try:
            profile = user.teacher_profile
            my_subjects = profile.subjects.all()
        except Exception:
            my_subjects = []

        context = {
            'my_subjects':     my_subjects,
            'total_students':  Student.objects.count(),
            'my_sessions':     Session.objects.filter(created_by=user).count(),
            'present_today':   Attendance.objects.filter(session__date=timezone.now().date(), session__created_by=user, status='present').count(),
        }
        return render(request, 'teacher/dashboard.html', context)

    # Student
    from students.models import Student
    from django.shortcuts import get_object_or_404
    try:
        student = user.student_profile
    except Exception:
        student = None
    return render(request, 'student/dashboard.html', {'student': student})
