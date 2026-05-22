from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login'), name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('students/', include('students.urls')),
    path('marks/', include('marks.urls')),
    path('fees/', include('fees.urls')),
    path('attendance/', include('attendance.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
