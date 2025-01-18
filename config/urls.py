from django.urls import include, path

urlpatterns = [
    path("accounts/", include('allauth.urls')),
    
    path("dashboard/", include('config.dashboard.urls')),
    path("", include("config.shorter.urls")),
]