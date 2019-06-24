# Importing required libraries
from django.urls import path
# Importing all view from views.py
from shop.views import *


# All url cases to process
urlpatterns = [
    # Basic url to enter the website
    path('', base_view, name='base'),
    path('category/<slug:category_slug>/', category_view, name='category_detail'),
    path('product/<slug:product_slug>/', product_view, name='product_detail'),
    path('order/<int:id>/', order_detail, name='order_detail'),
    path('order_process/<int:id>/', order_process, name='order_process'),
    path('user_profile/', user_profile_view, name='user_profile'),
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('confirm_order/<int:id>/', get_order_detail, name='confirm_order'),
    path('remove_from_cart_view/', remove_from_cart_view, name='remove_from_cart_view'),
    path('adjust_cart_item_quantity/', adjust_quantity, name='adjust_cart_item_quantity'),
    path('checkout/', checkout_view, name='checkout'),
    path('order/', order_view, name='order'),
    path('make_order/', make_order, name='make_order'),
    path('login_view/', login_view, name='login_view'),
    path('sign_in/', sign_in, name='sign_in'),
    path('sign_out/', sign_out, name='sign_out'),
    path('register_view/', register_view, name='register_view'),
    path('register/', register, name='register'),
]
