"""
URL configuration for emobilis_final project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from emobilis_final import settings
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('cart:view-cart', views.cart, name='cart'),
    path('cart:add-to-cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('cart:delete-from-cart/<int:item_id>', views.delete_cart_item, name='delete_from_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('contact', views.contact, name='contact'),
    path('product-details/<int:id>', views.product_details, name='product-details'),
    path('login', views.login_user, name='login'),
    path('privacy', views.privacy, name='privacy'),
    path('register', views.register, name='register'),
    path('settings', views.settings, name='settings'),
    path('shop', views.shop, name='shop'),
    path('terms', views.terms_and_conditions, name='terms'),
    path('transactions', views.transactions, name='transactions'),
    path('faq', views.faq, name='faq'),
    path('logout', views.logout_user, name='logout'),
    path('404', views.page_not_found, name='page_not_found'),
    path('order:complete', views.order_complete, name='order_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
