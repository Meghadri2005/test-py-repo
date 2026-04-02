from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
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


def return_policy(request):
    """Easy return policy page"""
    return render(request, 'accounts/return_policy.html')


def profile(request):
    """User profile page"""
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

# Create your views here.
