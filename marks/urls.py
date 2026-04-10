from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MarksViewSet, marks_view

router = DefaultRouter()
router.register('marks', MarksViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('marks/', marks_view, name='marks'),
]
