from rest_framework import serializers
from .models import Fee


class FeeSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Fee
        fields = ['id', 'student', 'student_id', 'amount', 'paid_amount',
                  'balance', 'status', 'due_date', 'description', 'created_at']

    def get_balance(self, obj):
        return obj.amount - obj.paid_amount
