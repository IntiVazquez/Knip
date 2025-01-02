from django.urls import path
from . import views
from .views import DashboardView, DeleteURLView

app_name = "dashboard"
urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path('delete/<int:url_id>/', DeleteURLView.as_view(), name='deleteURL'),
    path('edit/<int:url_id>/', views.editURL, name='editURL'),
]