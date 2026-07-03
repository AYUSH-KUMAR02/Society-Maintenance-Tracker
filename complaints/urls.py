from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('complaint/new/', views.raise_complaint, name='raise_complaint'),
    path('complaint/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('register/', views.register, name='register'),
    path('redirect-switch/', views.login_redirect_router, name='login_router'),
]