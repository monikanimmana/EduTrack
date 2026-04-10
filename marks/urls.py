from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MarksViewSet, marks_view

router = DefaultRouter()
router.register('', MarksViewSet, basename='marks')

urlpatterns = [
    path('api/', include(router.urls)),   # /marks/api/
    path('', marks_view, name='marks'),   # /marks/
]
