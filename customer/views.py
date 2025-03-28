from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout as auth_logout
from django.utils.cache import patch_cache_control
from django.views.decorators.cache import cache_control
from django.core.cache import cache
from .models import Customer
from wallet.models import Wallet

def landing_page(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        # Redirect to the profile page if the user is logged in
        return redirect('profile')
    return render(request, 'customer/index.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        
        customer = Customer(
            name=name,
            email=email,
            phone_number=phone_number,
            password=password
        )
        customer.save()
        return redirect('login') 
    return render(request, 'customer/register.html')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        try:
            customer = Customer.objects.get(email=email)
            # Use check_password to verify the hashed password
            if check_password(password, customer.password):
                # If the password matches, set the session (or redirect to profile)
                request.session['customer_id'] = customer.user_id # Store session or any required data
                response = redirect('profile')  # replace 'profile' with your actual profile view name
                patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)
                return response
            else:
                return render(request, 'customer/login.html', {'error': 'Invalid password'})
        except Customer.DoesNotExist:
            return render(request, 'customer/login.html', {'error': 'User does not exist'})

    return render(request, 'customer/login.html')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def profile(request):
    user_id = request.session.get('customer_id')
    
    try:
        # Fetch the Customer and Wallet by user_id
        customer = Customer.objects.get(user_id=user_id)
        wallet = Wallet.objects.get(customer=customer)  # Get the wallet associated with the customer
        response = render(request, 'customer/profile.html', {'customer': customer})
        patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)
        
        # Pass both customer and wallet to the template
        return render(request, 'customer/profile.html', {'customer': customer, 'wallet': wallet})
    except (Customer.DoesNotExist, Wallet.DoesNotExist):
        return redirect('login')  # Redirect to login if the customer or wallet doesn't exist

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def update_profile(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    
    customer = Customer.objects.get(user_id=customer_id)
    
    if request.method == 'POST':
        customer.name = request.POST['name']
        customer.email = request.POST['email']
        customer.phone_number = request.POST['phone_number']
        
        if request.POST['password']:
            customer.password = request.POST['password']  # Hashing will happen in the model's save method
        customer.save()
        return redirect('profile')
    
    return render(request, 'customer/update_profile.html', {'customer': customer})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def logout(request):
    # Clear the session and redirect to login
    auth_logout(request)
    request.session.flush()  # Ensure session data is cleared
    response = redirect('login')  # Redirect to the login page
    response.delete_cookie('sessionid')  # Extra precaution for session management
    return response

