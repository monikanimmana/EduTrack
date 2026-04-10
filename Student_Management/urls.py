from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth & dashboard
    path('auth/', include('users.urls')),
    path('', include('users.urls')),
    # Feature apps
    path('', include('students.urls')),
    path('', include('marks.urls')),
    path('', include('fees.urls')),
    path('', include('attendance.urls')),
    # Legacy Student app (kept for backward compat)
    path('legacy/', include('Student.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
