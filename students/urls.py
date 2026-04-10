from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, SubjectViewSet, StudentViewSet,
    student_list_view, student_profile_view,
    teacher_list_view, add_teacher_view,
)

router = DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('subjects', SubjectViewSet)
router.register('students', StudentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', student_list_view, name='student_list'),
    path('profile/', student_profile_view, name='student_profile'),
    path('teachers/', teacher_list_view, name='teacher_list'),
    path('teachers/add/', add_teacher_view, name='add_teacher'),
]
