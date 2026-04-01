from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from products.models import Product

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('welcome')

def welcome(request):
    """Landing/Welcome page for the site"""
    featured_products = Product.objects.filter(is_active=True)[:6]
    return render(request, 'accounts/welcome.html', {
        'featured_products': featured_products
    })

def home(request):
    """Home page for authenticated users"""
    return render(request, 'accounts/home.html')

def services(request):
    """Services page"""
    return render(request, 'accounts/services.html')

def contact(request):
    """Contact page"""
    return render(request, 'accounts/contact.html')

# Create your views here.
