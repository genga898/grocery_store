import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main_app import mpesa
from main_app.app_forms import LoginForm, MpesaPaymentForm, RegisterForm
from main_app.models import UserProfile, Product, Cart, Address, Orders
from django.contrib.auth.models import User as AuthUser


# Create your views here.
@login_required
def home(request):
    user = get_object_or_404(UserProfile, user=request.user)
    cart_items = Cart.objects.filter(user=user, is_removed=False).exclude(is_ordered=True)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'main_app/index.html', {"cart_items": cart_items, "total_price": total_price})


def about(request):
    return render(request, 'main_app/about.html')


@login_required
def cart(request):
    user = get_object_or_404(UserProfile, user=request.user)
    if user:
        cart_items = Cart.objects.filter(user=user, is_removed=False).exclude(is_ordered=True)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'main_app/cart.html', {"cart_items": cart_items, "total_price": total_price})
    return render(request, 'main_app/cart.html')


@login_required
def cart_header(request):
    user = get_object_or_404(UserProfile, user=request.user)
    if user:
        cart_items = Cart.objects.filter(user=user, is_removed=False).exclude(is_ordered=True)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'main_app/partials/navbar_cart.html',
                      {"cart_items": cart_items, "total_price": total_price})
    return render(request, 'main_app/partials/navbar_cart.html')


@login_required
def checkout(request):
    user = get_object_or_404(UserProfile, user=request.user)
    cart_items = Cart.objects.filter(user=user, is_removed=False).exclude(is_ordered=True)
    home_address = Address.objects.get(user=user)
    combined_address = f"{home_address.town}, {home_address.city}, {home_address.postal_code}"
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    phone_no = user.phone_number
    shipping_fee = 200
    total_item_cost = sum(item.product.price * item.quantity for item in cart_items)
    total_cost = shipping_fee + total_item_cost
    if request.method == 'POST' and (total_cost - shipping_fee) > 0:
        Orders.objects.create(user=user, total_cost=total_cost)
        for cart_item in cart_items:
            cart_item.is_ordered = True
            cart_item.save()
        return redirect('order_complete')
    else:
        return render(request, 'main_app/checkout.html', {"cart_items": cart_items, "total_item_cost": total_item_cost,
                                                          "shipping_fee": shipping_fee, "total": total_cost,
                                                          "phone_no": phone_no, "total_price": total_price,
                                                          "address": home_address, "full_address": combined_address
                                                          })


def contact(request):
    return render(request, 'main_app/contact.html')


@login_required
def product_details(request, id):
    product = Product.objects.get(pk=id)
    user = get_object_or_404(UserProfile, user=request.user)
    cart_items = Cart.objects.filter(user=user, is_removed=False).exclude(is_ordered=True)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'main_app/detail-product.html', {"product": product,
                                                            "cart_items": cart_items,
                                                            "total_price": total_price})


def faq(request):
    return render(request, 'main_app/faq.html')


def login_user(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'main_app/login.html', {"form": form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            UserProfile.user = authenticate(request, username=username, password=password)
            if UserProfile.user:
                login(request, UserProfile.user)
                messages.success(request, 'Welcome Back')
                return redirect('home')
        messages.error(request, 'Invalid username or password')
        return render(request, 'main_app/login.html', {"form": form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


def privacy(request):
    return render(request, 'main_app/privacy.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone_no = request.POST['contact']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user = AuthUser.objects.create_user(username=username, password=password, email=email, )
            new_user = UserProfile.objects.create(user=user, phone_number=phone_no)
            new_user.user.first_name = firstname
            new_user.user.last_name = lastname
            new_user.save()
            messages.success(request, "Registration successful")
            return redirect('login')
    return render(request, 'main_app/register.html')


def settings(request):
    user = get_object_or_404(UserProfile, user=request.user)
    phone_no = user.phone_number
    home_address = Address.objects.get(user=user)
    combined_address = f"{home_address.town}\n{home_address.city}\n{home_address.postal_code}"
    cart_items = Cart.objects.filter(user=user, is_removed=False).exclude(is_ordered=True)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        town = request.POST['town']
        country = request.POST['country']
        postcode = request.POST['postcode']
        address, created = Address.objects.get_or_create(user=user, town=town, city=country, postal_code=postcode)
        if created:
            messages.success(request, "Settings updated successfully")
            address.save()
    return render(request, 'main_app/setting.html', {"cart_items": cart_items,
                                                     "total_price": total_price,
                                                     "phone_number": phone_no,
                                                     "address": home_address,
                                                     "full_address": combined_address})


def shop(request):
    products = Product.objects.all().filter(quantity__gt=0)
    user = get_object_or_404(UserProfile, user=request.user)
    cart_items = Cart.objects.filter(user=user, is_removed=False).exclude(is_ordered=True)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'main_app/shop.html',
                  {"products": products, "cart_items": cart_items, "total_price": total_price})


def terms_and_conditions(request):
    return render(request, 'main_app/terms.html')


def transactions(request):
    user = get_object_or_404(UserProfile, user=request.user)
    cart_items = Cart.objects.filter(user=user, is_removed=False).exclude(is_ordered=True)
    orders = Orders.objects.filter(user=user)
    ordered_items = Cart.objects.filter(user=user, is_ordered=True).exclude(is_removed=True)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    shipping_fee = 200
    ordered_items_cost = sum(item.product.price * item.quantity for item in ordered_items)
    total_cost = shipping_fee + ordered_items_cost
    return render(request, 'main_app/transaction.html',
                  {"cart_items": cart_items,
                   "total_price": total_price,
                   "ordered_items": ordered_items,
                   "items_cost": ordered_items_cost,
                   "shipping_fee": shipping_fee,
                   "total": total_cost,
                   "orders": orders})


@login_required
def add_to_cart(request, product_id):
    user = get_object_or_404(UserProfile, user=request.user)
    product = Product.objects.get(pk=product_id)
    cart_product = Cart.objects.filter(user=user, product=product_id, is_removed=False).exclude(is_ordered=True).first()
    if cart_product:
        cart_product.quantity += 1
        cart_product.save()
    else:
        Cart.objects.create(product=product, user=user)
    return redirect('cart')


@login_required
def delete_cart_item(request, item_id):
    cart_item = Cart.objects.get(pk=item_id)
    cart_item.is_removed = True
    cart_item.save()
    return redirect('cart')


def page_not_found(request):
    return render(request, 'main_app/404.html')


@login_required
def order_complete(request):
    user = get_object_or_404(UserProfile, user=request.user)
    cart_items = Cart.objects.filter(user=user, is_removed=False).exclude(is_ordered=True)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'main_app/mpesa payment.html',
                  {"cart_items": cart_items,
                   "total_price": total_price})
