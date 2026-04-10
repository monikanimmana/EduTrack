from rest_framework import serializers
from .models import Session, Attendance


class SessionSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    qr_valid = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'subject', 'subject_name', 'date', 'start_time',
                  'end_time', 'qr_token', 'qr_valid_until', 'is_active', 'qr_valid']
        read_only_fields = ['qr_token']

    def get_qr_valid(self, obj):
        return obj.is_qr_valid()


class AttendanceSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    session_info = serializers.StringRelatedField(source='session', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'session', 'session_info', 'student', 'student_id',
                  'status', 'method', 'marked_at']
        read_only_fields = ['marked_at']


class QRAttendanceSerializer(serializers.Serializer):
    qr_token = serializers.UUIDField()
