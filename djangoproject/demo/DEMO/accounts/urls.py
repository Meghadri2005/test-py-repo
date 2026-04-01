from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
]