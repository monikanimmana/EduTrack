from rest_framework import serializers
from .models import Marks


class MarksSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    percentage = serializers.ReadOnlyField()
    grade = serializers.ReadOnlyField()

    class Meta:
        model = Marks
        fields = ['id', 'student', 'student_id', 'subject', 'subject_name',
                  'score', 'max_score', 'percentage', 'grade', 'exam_date', 'remarks']
