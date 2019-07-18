# A library to send emails
import smtplib
# Importing required fields from settings.py to send emails
from project.settings import USERNAME, PASSWORD, MAIL_HOST, MAIL_PORT, SHOP_ADDRESS
# Django created User model
from django.contrib.auth.models import User
# Methods to return a response from server to client
from django.shortcuts import render, redirect
from django.http import JsonResponse
# Methods to handle authorization
from django.contrib.auth import authenticate, login, logout
# Decorator to require authorization of user
from django.contrib.auth.decorators import login_required
# Forms to handle registration and Order
from shop.forms import RegistrationForm, OrderForm
# Models to interact
from shop.models import Category, Product, Cart, CartItem, Order


# Create your views here.


# A function to return base html page
def base_view(request):
    context = {}
    # Determining user type manager or customer
    if not hasattr(request.user, 'manager'):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'categories': categories,
            'products': products,

        }
        # Returning appropriate response
        return render(request, 'index.html', context)
    else:
        # Returning appropriate response
        order = Order.objects.filter(status='Accepted')
        context['order'] = order
        return render(request, 'manager.html', context)


# A function to return a page to login
def login_view(request):
    return render(request, 'login.html')


# Function to return registration form
def register_view(request):
    form = RegistrationForm()
    context = {'form': form}
    return render(request, 'register.html', context)


# A function to handle registration of user
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # Form validation
        if form.is_valid():
            print(form.cleaned_data)
            # Creating a new user
            form.save()
            return redirect(base_view)
        else:
            form = RegistrationForm()
            context = {'form': form}
            return render(request, 'register.html', context)


# A function to handle authorization
def sign_in(request):
    context = {}
    if request.POST:
        # Retrieving user data from request
        username = request.POST['username']
        password = request.POST['password']
        # Authenticating the user with following username and password
        user = authenticate(username=username, password=password)
        # Checking login and password
        if user is not None:
            # Logging-in the user
            login(request, user)
            login_user = User.objects.get(username=username)
            # Determining the user type manager or customer
            if hasattr(login_user, 'manager'):
                return redirect('/')
            else:
                try:
                    # Getting or creating a cart for user
                    c = Cart.objects.get_or_create(owner=user)
                    context['cart'] = c
                # Handling exception if multiple carts were found
                except Cart.MultipleObjectsReturned:
                    # Returning the last cart of the user
                    c = Cart.objects.filter(owner=user).last()
                    context['cart'] = c
                return redirect(base_view)
        # Returning appropriate response if user authorization was unsuccessful
        else:
            context['login_error'] = "Incorrect username or password"
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html', context)


# A function to handle logging-out of user
def sign_out(request):
    logout(request)
    return redirect(base_view)


# Returning a certain product
def product_view(request, product_slug):
    categories = Category.objects.all()
    product = Product.objects.get(slug=product_slug)
    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'product.html', context)


# returning a certain category according to request
def category_view(request, category_slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug=category_slug)
    products_of_category = Product.objects.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products_of_category': products_of_category

    }
    return render(request, 'category.html', context)


# A function to return a cart or user and rendering html page of user's cart
@login_required()
def cart_view(request):
    categories = Category.objects.all()
    try:
        cart = Cart.objects.get(owner=request.user)
    except Cart.MultipleObjectsReturned:
        cart = Cart.objects.filter(owner=request.user).last()
    context = {
        'categories': categories,
        'cart': cart

    }
    return render(request, 'cart.html', context)


# A function to handle adding items to cart
@login_required()
def add_to_cart_view(request):
    # Handling AJAX request from client
    if request.is_ajax():
        user = request.user
        product = Product.objects.get(slug=request.GET['product_slug'])
        cart = Cart.objects.filter(owner=user).last()
        cart_item, status = CartItem.objects.get_or_create(product=product, cart=cart)
        # If cart item alredy exist just increment quantity of the item
        if not status:
            cart_item.quantity += 1
            # Saving changes in database
            cart_item.save()
        return JsonResponse({'product': str(cart_item.product), 'quantity': str(cart_item.quantity)}, safe=False)


# # Function to handle removing items from cart
@login_required()
def remove_from_cart_view(request):
    # Handling AJAX request from client
    if request.is_ajax():
        cart = Cart.objects.filter(owner=request.user).last()
        CartItem.objects.get(id=int(request.GET['cart_item_id'])).delete()
        return JsonResponse({'count': str(Cart.objects.get_or_create(owner=request.user)[0].cartitem_set.count()),
                             'cart_total': cart.get_cart_total()})


# A function to adjust quantity of items in cart
@login_required()
def adjust_quantity(request):
    # Handling AJAX request from client
    if request.is_ajax():
        cart = Cart.objects.filter(owner=request.user).last()
        cart_item = CartItem.objects.get(id=int(request.GET['cart_item_id']))
        # Setting a quantity of cart item
        cart_item.quantity = int(request.GET['cart_item_quantity'])
        # Sving all changes in database
        cart_item.save()
        return JsonResponse({'total': cart_item.quantity*cart_item.product.price, 'cart_total': cart.get_cart_total()})


# Returning checkout page
@login_required()
def checkout_view(request):
    cart = Cart.objects.filter(owner=request.user).last()
    context = {
        'cart': cart
    }
    return render(request, 'checkout.html', context)


# Returning ordering page
@login_required()
def order_view(request):
    cart = Cart.objects.filter(owner=request.user).last()
    order_form = OrderForm()
    context = {
        'cart': cart,
        'order_form': order_form
    }
    return render(request, 'order.html', context)


# A function to handle making order from client
@login_required()
def make_order(request):
    user = request.user
    cart = Cart.objects.filter(owner=user).last()
    order_form = OrderForm(request.POST)
    # Form validation
    if order_form.is_valid():
        phone = order_form['phone'].value()
        buy_type = order_form['buy_type'].value()
        address = order_form['address'].value()
        comments = order_form['comments'].value()
        # Setting default status of order
        status = 'Accepted'
        order = Order.objects.get_or_create(user=user, items=cart, phone=phone, address=address,
                                            buy_type=buy_type, comments=comments, status=status)
        if order[1]:
            order[0].save()
            new_cart = Cart.objects.create(owner=user)
            # Creating new cart for user after order
            new_cart.save()
            # Sending emails after making order
            server = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
            server.ehlo()
            server.starttls()
            server.login(USERNAME, PASSWORD)
            # Txt of email
            message = 'Dear {0}! Your order has been accepted. Please wait until our manager will process ' \
                      'your order. You will get an email notification after your order will be ready to ' \
                      'deliver or pickup'.format(user.username)
            server.sendmail(USERNAME, user.email, message)
            server.quit()

    return render(request, 'order_final.html')


# A function to return details of a certain order item
def order_detail(request, id):
    order = Order.objects.get(id=id)
    context = {
        'order': order
    }
    return render(request, 'order_process.html', context)


# A function to process order for manager
def order_process(request, id):
    global order_delivery
    order = Order.objects.get(id=int(id))
    username = order.user.username
    email = order.user.email
    order.status = 'Waiting for the recipient'
    order.save()
    # Determining buying type and setting a certain message for email
    if order.buy_type == 'Pickup':
        order_delivery = 'is ready to pickup. You can get your order from address {0}'.format(SHOP_ADDRESS)
    else:
        order_delivery = 'has been sent by courier. Soon, your order will be delivered.'
    # Sending email to notify user
    server = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(USERNAME, PASSWORD)
    message = ('Dear {0}! Your order ' + order_delivery).format(username)
    server.sendmail(USERNAME, email, message)
    server.quit()
    return redirect(base_view)


# A function to return profile page of user
def user_profile_view(request):
    context = {}
    order = Order.objects.filter(user=request.user)
    context['order'] = order
    return render(request, 'user_profile.html', context)


# Function to return page for certain order item
def get_order_detail(request, id):
    user = request.user
    order = Order.objects.get(id=id)
    # Setting new status for order
    order.status = 'Handed over'
    order.save()
    server = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(USERNAME, PASSWORD)
    message = ('Dear {0}! Thank you for using our services. We really hope that you like our '
               'services and the quality of goods.').format(user.username)
    server.sendmail(USERNAME, user.email, message)
    server.quit()
    return redirect(user_profile_view)




