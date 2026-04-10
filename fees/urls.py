from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeeViewSet, fees_view

router = DefaultRouter()
router.register('', FeeViewSet, basename='fees')

urlpatterns = [
    path('api/', include(router.urls)),   # /fees/api/
    path('', fees_view, name='fees'),     # /fees/
]
