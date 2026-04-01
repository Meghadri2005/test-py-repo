from django.urls import path
from . import views

urlpatterns = [
    # Public product views
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),

    # Admin product management views
    path('admin/', views.admin_product_list, name='admin_product_list'),
    path('admin/create/', views.product_create, name='product_create'),
    path('admin/<int:pk>/update/', views.product_update, name='product_update'),
    path('admin/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('admin/<int:pk>/toggle/', views.product_toggle_status, name='product_toggle'),
]