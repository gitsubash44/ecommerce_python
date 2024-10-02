from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import Customer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')  # Add password retrieval
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request,"Login failed ! Try again")
            # Optionally, add some error message here for failed login attempts
            print("Invalid credentials")
    
    return render(request, 'accounts/login.html')


def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone_field')
        confirm_password = request.POST.get('confirm_password')

        # Validate that passwords match
        if password == confirm_password:
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists!")
                return redirect('user_register')
            # Check if the email already exists
            elif User.objects.filter(email=email).exists():
                messages.info(request,"This email is already registered.!")
                return redirect('user_register')
            else:
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()  # Save the user instance

                # Save additional customer information
                customer = Customer(user=user, phone_field=phone)
                customer.save()

                # Log the user in after registration
                our_user = authenticate(username=username, password=password)
                if our_user is not None:
                    login(request, our_user)
                    return redirect('index')
        else:
            messages.info(request,"Confirm_Password do not match!")
            print("Passwords do not match!")
            return redirect('user_register')
    
    return render(request, 'accounts/register.html')


def user_logout(request):
    logout(request)
    return redirect('index')
