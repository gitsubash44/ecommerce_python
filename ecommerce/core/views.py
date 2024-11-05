from django.shortcuts import redirect, render
from core.forms import ProductForm
from django.contrib import messages
from core.models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html',{'products':products})


def orderlist(request):
    if Order.objects.filter(user=request.user,ordered=False).exists():
        order = Order.objects.grt(user = request.user,ordered=False)
        return render(request,'orderlist.html',{'order':order})
    return render(request,'orderlist.html',{'message':"Your Cart is Empty"})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully")
            return redirect('/')
        else:
            print(form.errors)  # This will print errors to the console
            messages.error(request, "Product is not added due to errors.")
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def product_desc(request,pk):
    product = Product.objects.get(pk=pk)
    return render(request,'product_desc.html',{'product':product})
    


def add_to_cart(request,pk):
    # get that particular product of id = pk
    product = Product.objects.get(pk=pk)
    # create order item 
    order_item, created  = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False,
    )
    
    # Get query set of order object of particular user
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists(): 
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, "Added quantity Item. ")
            return redirect("product_desc",pk=pk)
        else:
            order_item.add(order_item,)
            messages.info(request,"Item added to cart")   
            return redirect("product_desc",pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item Added To Cart")
        return  redirect("product_desc",pk=pk) 
    
    
def add_item(request,pk):
    # get that particular product of id = pk
    product = Product.objects.get(pk=pk)
    # create order item 
    order_item, created  = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False,
    )
    
    # Get query set of order object of particular user
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists(): 
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity +=1
                order_item.save()
                messages.info(request, "Added quantity Item. ")
                return redirect("orderlist")
            else:
                messages.info(request,"Sorry!, Product is out of stock")
                return redirect("orderlist")
        else:
            order_item.add(order_item,)
            messages.info(request,"Item added to cart")   
            return redirect("product_desc",pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item Added To Cart")
        return  redirect("product_desc",pk=pk) 
    
    
def remove_item(request):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False,
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(Product__pk=pk).exists():
            order_item = OrderItem.objects.filter(
                product = item,
                user = request.user,
                ordered = False,
            )