from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SessionViewSet, AttendanceViewSet, QRScanView, attendance_view, qr_scan_view

router = DefaultRouter()
router.register('sessions', SessionViewSet)
router.register('attendance', AttendanceViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/qr-scan/', QRScanView.as_view(), name='qr_scan_api'),
    path('attendance/', attendance_view, name='attendance'),
    path('attendance/scan/<uuid:token>/', qr_scan_view, name='qr_scan'),
]
