from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path ('managers/', views.manager_approval, name='manager_approve_products'),
    
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    path('customers/', views.customer_list, name='customer_list'),
    # path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),

    path('orders/', views.order_list, name='order_list'),
    path('orders-details/<int:pk>/', views.order_detail, name='order_detail'),
   
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # path('sellers/', views.seller_list, name='seller_list'),
    # path('sellers/<int:pk>/', views.seller_detail, name='seller_detail'),

    path('seller/products/', views.seller_products, name='seller_products'),
    path('seller/add_product/', views.add_product, name='add_product'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('seller/remove_product/<int:product_id>/', views.remove_product_from_seller, name='remove_product_from_seller'),
    
    
   

]