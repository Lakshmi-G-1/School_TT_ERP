from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1. The Django Admin Site
    path('admin/', admin.site.urls),

    # 2. Your School ERP App URLs
    path('', include('timetable.urls')),

    # 3. Built-in Login/Logout System
    path('accounts/', include('django.contrib.auth.urls')),
]