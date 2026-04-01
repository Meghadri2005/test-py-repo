from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, Review
from .forms import ProductForm

def is_admin(user):
    return user.is_staff or user.is_superuser

def product_list(request):
    """Public view to display all active products"""
    products = Product.objects.filter(is_active=True)
    paginator = Paginator(products, 12)  # Show 12 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'is_admin_view': False
    })

def product_detail(request, pk):
    """Detailed view of a single product with reviews"""
    # Get product - allow inactive products for admins, but show 404 to regular users
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        from django.http import Http404
        raise Http404("Product not found")
    
    # If product is inactive and user is not admin, return 404
    if not product.is_active and not (request.user.is_staff or request.user.is_superuser):
        from django.http import Http404
        raise Http404("Product not found")
    
    reviews = product.reviews.all()
    user_review = None
    
    if request.user.is_authenticated:
        user_review = product.reviews.filter(user=request.user).first()
    
    # Handle review submission
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        
        if rating and title and comment:
            # Update existing review or create new
            review, created = Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': int(rating),
                    'title': title,
                    'comment': comment,
                }
            )
            action = "added" if created else "updated"
            messages.success(request, f'Your review has been {action} successfully!')
            return redirect('product_detail', pk=product.pk)
        else:
            messages.error(request, 'Please fill in all fields.')
    
    context = {
        'product': product,
        'reviews': reviews,
        'user_review': user_review,
        'average_rating': product.average_rating(),
        'review_count': product.review_count(),
    }
    
    return render(request, 'products/product_detail.html', context)

@user_passes_test(is_admin)
def admin_product_list(request):
    """Admin view to manage all products"""
    products = Product.objects.all().order_by('-created_at')
    paginator = Paginator(products, 20)  # Show 20 products per page for admin

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/admin_product_list.html', {
        'page_obj': page_obj,
        'total_products': products.count(),
        'active_products': products.filter(is_active=True).count()
    })

@user_passes_test(is_admin)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, f'Product "{product.name}" has been created successfully!')
            return redirect('admin_product_list')
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Add New Product',
        'button_text': 'Create Product'
    })

@user_passes_test(is_admin)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" has been updated successfully!')
            return redirect('admin_product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': f'Edit Product: {product.name}',
        'button_text': 'Update Product'
    })

@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted successfully!')
        return redirect('admin_product_list')

    return render(request, 'products/product_confirm_delete.html', {
        'product': product
    })

@user_passes_test(is_admin)
def product_toggle_status(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_active = not product.is_active
    product.save()
    status = "activated" if product.is_active else "deactivated"
    messages.success(request, f'Product "{product.name}" has been {status}!')
    return redirect('admin_product_list')
