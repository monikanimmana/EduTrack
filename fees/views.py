from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Fee
from .serializers import FeeSerializer
from users.permissions import IsTeacherOrReadOnly
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
    user = request.user

    if user.is_admin() or user.is_teacher():
        fees = Fee.objects.select_related('student__user').all()

        # summary stats
        from django.db.models import Sum, Count
        total_amount  = fees.aggregate(t=Sum('amount'))['t'] or 0
        total_paid    = fees.aggregate(t=Sum('paid_amount'))['t'] or 0
        count_paid    = fees.filter(status='paid').count()
        count_unpaid  = fees.filter(status='unpaid').count()
        count_partial = fees.filter(status='partial').count()

        # filter by status
        status_filter = request.GET.get('status', '')
        if status_filter:
            fees = fees.filter(status=status_filter)

        # search
        search = request.GET.get('q', '')
        if search:
            fees = fees.filter(student__student_id__icontains=search) | \
                   fees.filter(student__user__first_name__icontains=search) | \
                   fees.filter(student__user__last_name__icontains=search)

        return render(request, 'teacher/fees.html', {
            'fees': fees,
            'total_amount':  total_amount,
            'total_paid':    total_paid,
            'total_due':     total_amount - total_paid,
            'count_paid':    count_paid,
            'count_unpaid':  count_unpaid,
            'count_partial': count_partial,
            'status_filter': status_filter,
            'search':        search,
        })

    # Student
    student = get_object_or_404(Student, user=user)
    fees = Fee.objects.filter(student=student)
    return render(request, 'student/fees.html', {'fees': fees})
