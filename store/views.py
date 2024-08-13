from django.shortcuts import render,redirect
from django.http import JsonResponse

import json
import datetime
import logging

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, auth
from .models import *
from .utils import cookieCart, cartData, guestOrder

def main(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request,'store/main.html', context)

def log_use(request,cp_name):
    username=cp_name
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    
    if request.user.is_authenticated:
        context['username'] = username
        return render(request, 'store/store.html', context)
    else:
        return render(request, 'store/store.html', context)
    
def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def order(request):
    if request.method == "POST":
        # Extract data from POST request using .get() method
        username = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        # Save to the database
        data = UserAddress(username=username,email=email,street=street, city=city,state=state, pincode=pincode)
        data.save()

    return redirect('store')

from django.db import IntegrityError

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not all([username, email, password1, password2]):
            messages.error(request, 'All fields are required')
            return render(request, 'store/register.html')

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            else:
                try:
                    # Create the user
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    
                    # Create associated Customer object
                    Customer.objects.create(user=user)
                    
                    # Log in the user after registration
                    auth.login(request, user)  
                    
                    capitalized_username = user.username.capitalize()
                    return render(request, 'store.html', {'username': capitalized_username})
                except IntegrityError:
                    messages.error(request, 'Account created login below..')
        else:
            messages.error(request, 'Passwords do not match')
        
        return render(request, 'store/register.html')
    return render(request, 'store/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            cp_name = user.username.capitalize()
            return log_use(request,cp_name)
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'store/login.html')
    else:
        return render(request, 'store/login.html')

def logout(request):
    auth.logout(request)
    return redirect('store')

def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.profile.address = request.POST.get('address')
        user.save()
        return redirect('profile')

    return render(request, 'store/profile.html', {
        'user': request.user,
        'username': request.user.username,
        'cartItems': cartData(request)['cartItems']
    })

def navbar(request):
    return render(request, 'store/navbar.html')

def contact_us(request):
    return render(request, 'store/contact_us.html')

def about_us(request):
    return render(request, 'store/about_us.html')

def faq(request):
    return render(request, 'store/faq.html')

def track(request):
    return render(request, 'store/track.html')

def returns(request):
    return render(request, 'store/return.html')

def offer(request):
    return render(request, 'store/offer.html')

def gift(request):
    return render(request, 'store/gift.html')

def career(request):
    return render(request, 'store/career.html')

def press(request):
    return render(request, 'store/press.html')

def blog(request):
    return render(request, 'store/blog.html')

def order_history(request):
    orders = Order.objects.filter(customer=request.user.customer)
    return render(request, 'store/order_history.html', {'orders': orders})


def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.profile.address = request.POST.get('address')
        user.save()
        messages.success(request, 'Your profile was successfully updated!')
        return redirect('update_profile')
    return render(request, 'store/update_profile.html', {'user': request.user})

def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was updated successfully!')
            return redirect('store/profile')
        else:
            messages.error(request, 'An error occurred!')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'store/update_password.html', {'form': form})

def track_order(request):
    return redirect('store')