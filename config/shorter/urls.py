from django.urls import path

from . import views

app_name = "shorter"
urlpatterns = [
    path("", views.home, name = "home"),
    path("<str:short_url>/", views.redirectURL, name = "redirectURL"),
]