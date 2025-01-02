from django.contrib import admin
from django.urls import include, path

from config.dashboard.views import DashboardView 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include('allauth.urls')),
    
    path("dashboard/", include('config.dashboard.urls')),
    path("", include("config.shorter.urls")),
]