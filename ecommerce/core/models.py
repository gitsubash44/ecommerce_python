from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import *

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    phone_field = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    desc = models.TextField()
    price = models.FloatField(default=0.0)
    product_available_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def get_add_to_cart_url(self):
        return reverse("core:add_to_cart", kwargs={
            "pk": self.pk
        })
        
    def __str__(self):
        return self.name


class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
def __str__(self):
    return f"{self.quantity} of {self.product.name}"

def get_total_item_price(self):
    return self.quantity * self.product.price

def get_final_price(self):
    return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100,unique=True,default=None,blank=True,null=True)
    datetime_ofpayment = models.DateTimeField(auto_now_add=True)
    order_delivered = models.BooleanField(default=False)
    order_received = models.BooleanField(default=False)
    
    def save(self,*args, **kwargs):
        if self.order_id is None and self.datetime_ofpayment and self.id:
            self.order_id = self.datetime_ofpayment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
            
        return super().save(*args, **kwargs)

def __str__(self):
    return self.user.username

def get_total_price(self):    
    total = 0
    for order_item in self.items.all():
        total += order_item.get_final_price()
    return total

def get_total_count(self):
    order = order.objects.get(pk=self.pk)
    return order.items.count()