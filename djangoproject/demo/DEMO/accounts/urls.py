from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('services/', views.services, name='services'),
    path('return-policy/', views.return_policy, name='return_policy'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
]