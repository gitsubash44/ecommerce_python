from django.shortcuts import redirect, render
from core.forms import ProductForm
from django.contrib import messages
from core.models import *
# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html',{'products':products})

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
