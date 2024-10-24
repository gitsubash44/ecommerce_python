from django.shortcuts import redirect, render
from core.forms import *
# Create your views here.
def index(request):
    return render(request, 'index.html')

def add_product(request):
    if request.method == 'POST':
        form  = ProductForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form' : form})