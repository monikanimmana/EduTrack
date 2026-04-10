from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SessionViewSet, AttendanceViewSet, QRScanView, attendance_view, qr_scan_view, session_qr_view, session_records_view

router = DefaultRouter()
router.register('sessions', SessionViewSet)
router.register('records', AttendanceViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/qr-scan/', QRScanView.as_view(), name='qr_scan_api'),
    path('', attendance_view, name='attendance'),
    path('scan/<uuid:token>/', qr_scan_view, name='qr_scan'),
    path('session/<int:session_id>/qr/', session_qr_view, name='session_qr'),
    path('session/<int:session_id>/records/', session_records_view, name='session_records'),
]
