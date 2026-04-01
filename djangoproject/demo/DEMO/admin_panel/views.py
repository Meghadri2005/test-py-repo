from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from products.models import Product


def is_admin_user(user):
    """Check if user is admin or staff"""
    return user.is_active and (user.is_staff or user.is_superuser)


def admin_login(request):
    """Admin login page"""
    if request.user.is_authenticated and is_admin_user(request.user):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You do not have admin access.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'admin_panel/admin_login.html')


@login_required(login_url='admin_login')
@user_passes_test(is_admin_user, login_url='admin_login')
def admin_dashboard(request):
    """Admin dashboard with analytics"""
    
    # Get statistics
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    total_stock = Product.objects.aggregate(Sum('stock'))['stock__sum'] or 0
    total_revenue = Product.objects.aggregate(Sum('price'))['price__sum'] or 0
    
    # Get recent products
    recent_products = Product.objects.all().order_by('-created_at')[:5]
    
    # Get all users
    total_users = User.objects.count()
    admin_users = User.objects.filter(is_staff=True).count()
    active_users = User.objects.filter(is_active=True).count()
    
    # Low stock products (less than 10)
    low_stock_products = Product.objects.filter(stock__lt=10, is_active=True)
    
    context = {
        'total_products': total_products,
        'active_products': active_products,
        'total_stock': total_stock,
        'total_revenue': total_revenue,
        'recent_products': recent_products,
        'total_users': total_users,
        'admin_users': admin_users,
        'active_users': active_users,
        'low_stock_products': low_stock_products.count(),
        'low_stock_list': low_stock_products[:5],
    }
    
    return render(request, 'admin_panel/admin_dashboard.html', context)


@login_required(login_url='admin_login')
@user_passes_test(is_admin_user, login_url='admin_login')
def manage_users(request):
    """Manage users - view list and update admin status"""
    users = User.objects.all().order_by('-date_joined')
    
    # Handle admin status toggle
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        
        try:
            user = User.objects.get(id=user_id)
            
            if action == 'make_admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()
                messages.success(request, f'{user.username} is now an admin.')
            elif action == 'remove_admin':
                user.is_staff = False
                user.is_superuser = False
                user.save()
                messages.success(request, f'{user.username} is no longer an admin.')
            elif action == 'deactivate':
                user.is_active = False
                user.save()
                messages.success(request, f'{user.username} has been deactivated.')
            elif action == 'activate':
                user.is_active = True
                user.save()
                messages.success(request, f'{user.username} has been activated.')
            elif action == 'delete':
                username = user.username
                user.delete()
                messages.success(request, f'User {username} has been deleted.')
                return redirect('manage_users')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        
        return redirect('manage_users')
    
    context = {
        'users': users,
        'total_users': users.count(),
        'active_users': users.filter(is_active=True).count(),
        'admin_users': users.filter(is_staff=True).count(),
    }
    
    return render(request, 'admin_panel/manage_users.html', context)


@login_required(login_url='admin_login')
@user_passes_test(is_admin_user, login_url='admin_login')
def analytics(request):
    """Analytics page with detailed statistics"""
    
    # Product analytics
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    inactive_products = Product.objects.filter(is_active=False).count()
    total_stock = Product.objects.aggregate(Sum('stock'))['stock__sum'] or 0
    
    # Price analytics
    avg_price = Product.objects.aggregate(avg_price=Sum('price') / Count('id'))['avg_price'] or 0
    highest_price_product = Product.objects.order_by('-price').first()
    lowest_price_product = Product.objects.order_by('price').first()
    
    # Stock analytics
    out_of_stock = Product.objects.filter(stock=0).count()
    low_stock = Product.objects.filter(stock__gt=0, stock__lt=10).count()
    well_stocked = Product.objects.filter(stock__gte=10).count()
    
    # Top products (by stock or price)
    top_stocked = Product.objects.order_by('-stock')[:5]
    expensive_products = Product.objects.order_by('-price')[:5]
    
    context = {
        'total_products': total_products,
        'active_products': active_products,
        'inactive_products': inactive_products,
        'total_stock': total_stock,
        'avg_price': round(float(avg_price), 2) if avg_price else 0,
        'highest_price_product': highest_price_product,
        'lowest_price_product': lowest_price_product,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        'well_stocked': well_stocked,
        'top_stocked': top_stocked,
        'expensive_products': expensive_products,
    }
    
    return render(request, 'admin_panel/analytics.html', context)


@login_required(login_url='admin_login')
@user_passes_test(is_admin_user, login_url='admin_login')
def admin_logout(request):
    """Admin logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('admin_login')
