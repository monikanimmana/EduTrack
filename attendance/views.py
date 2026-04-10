import io
import qrcode
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Session, Attendance
from .serializers import SessionSerializer, AttendanceSerializer, QRAttendanceSerializer
from users.permissions import IsTeacher, IsTeacherOrReadOnly
from students.models import Student


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related('subject').all()
    serializer_class = SessionSerializer
    permission_classes = [IsTeacher]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['subject', 'date', 'is_active']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def qr_image(self, request, pk=None):
        session = self.get_object()
        qr_url = request.build_absolute_uri(f'/attendance/scan/{session.qr_token}/')
        img = qrcode.make(qr_url)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return HttpResponse(buf.getvalue(), content_type='image/png')


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('session', 'student').all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsTeacherOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['session', 'student', 'status', 'method']
    search_fields = ['student__student_id']

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_student():
            student = get_object_or_404(Student, user=self.request.user)
            return qs.filter(student=student)
        return qs


class QRScanView(APIView):
    """Student scans QR code to mark attendance."""
    def post(self, request):
        serializer = QRAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['qr_token']

        session = get_object_or_404(Session, qr_token=token, is_active=True)
        if not session.is_qr_valid():
            return Response({'error': 'QR code has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        student = get_object_or_404(Student, user=request.user)
        if Attendance.objects.filter(session=session, student=student).exists():
            return Response({'error': 'Attendance already marked.'}, status=status.HTTP_400_BAD_REQUEST)

        Attendance.objects.create(
            session=session, student=student,
            status=Attendance.STATUS_PRESENT, method=Attendance.METHOD_QR
        )
        return Response({'message': 'Attendance marked successfully.'}, status=status.HTTP_201_CREATED)


# ── HTML Views ───────────────────────────────────────────────────────────────

@login_required
def attendance_view(request):
    if request.user.is_teacher():
        sessions = Session.objects.select_related('subject').all()
        return render(request, 'teacher/attendance.html', {'sessions': sessions})
    student = get_object_or_404(Student, user=request.user)
    records = Attendance.objects.filter(student=student).select_related('session__subject')
    return render(request, 'student/attendance.html', {'records': records})


@login_required
def qr_scan_view(request, token):
    session = get_object_or_404(Session, qr_token=token, is_active=True)
    return render(request, 'student/qr_scan.html', {'session': session, 'token': token})
