import os
import uuid

from django.contrib.auth.models import User as AuthUser
from django.db import models


def generate_unique_name(instance, filename):
    name = uuid.uuid4()  # universally unique id
    ext = filename.split(".")[-1]
    full_filename = f"{name}.{ext}"
    return os.path.join("products", full_filename)


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    town = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city}\n{self.town}\n{self.postal_code}"


class Categories(models.Model):
    name = models.CharField(max_length=100)
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Added At")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Last modified")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=generate_unique_name, blank=False)
    shipping_fee = models.IntegerField(default=200)
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name,

    def get_price(self):
        return self.product.price * self.quantity


class Payment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Orders(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(
        auto_now_add=True
    )

