# currency_exchange/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from .models import CurrencyExchange
from wallet.models import Wallet
from admin_panel.models import AdminSettings  # Import AdminSettings model
from customer.models import Customer
import currencyapicom
from django.views.decorators.cache import never_cache , cache_control
from django.contrib.auth import logout as auth_logout
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.http import JsonResponse

API_KEY= "XXXXXXXXXXXXXXXX" #get your api key from currencyapi.com
currency_client = currencyapicom.Client(API_KEY)

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@never_cache
def exchange_currency(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')

    if request.method == 'POST':
        # Retrieve form data
        sell_currency = request.POST.get('sell_currency')
        buy_currency = request.POST.get('buy_currency')
        amount_sold = Decimal(request.POST.get('amount'))

        # Get wallet for the logged-in user
        customer_id = request.session.get('customer_id')
        try:
            customer = Customer.objects.get(user_id=customer_id)
        except Customer.DoesNotExist:
            messages.error(request, "Customer not found. Please log in again.")
            return redirect('login')
        wallet = Wallet.objects.get(customer=customer)
        
        # Check wallet balance and validate amount
        balance = getattr(wallet, f'balance_{sell_currency.lower()}')
        if balance == 0:
            messages.error(request, f"No balance available in {sell_currency} wallet.")
            return redirect('exchange_currency')
        elif amount_sold > balance:
            messages.error(request, "Amount exceeds available balance.")
            return redirect('exchange_currency')
        
        # Fetch exchange rate using CurrencyAPI with the correct method
        try:
            rate_data = currency_client.latest([sell_currency], [buy_currency])
            rate = Decimal(rate_data['data'][buy_currency]['value'])
        except Exception as e:
            messages.error(request, f"Error fetching exchange rate: {e}")
            return redirect('exchange_currency')
        
        # Fetch the profit margin from the admin settings table
        try:
            admin_settings = AdminSettings.objects.get(id=1)
            profit_margin = admin_settings.profit_margin
        except AdminSettings.DoesNotExist:
            profit_margin = Decimal(0.02)  # Default to 2% if not set
        
        # Calculate adjusted rate with profit margin
        adjusted_rate = rate * (1 - profit_margin)
        amount_bought = amount_sold * adjusted_rate

        context = {
            'sell_currency': sell_currency,
            'buy_currency': buy_currency,
            'amount_sold': amount_sold,
            'amount_bought': amount_bought,
            'rate': adjusted_rate,
        }
        
        return render(request, 'currency_exchange/confirm_exchange.html', context)
    
    return render(request, 'currency_exchange/exchange_form.html')



def confirm_exchange(request):
    if request.method == 'POST':
        customer_id = request.session.get('customer_id')
        sell_currency = request.POST['sell_currency']
        buy_currency = request.POST['buy_currency']
        amount_sold = Decimal(request.POST['amount_sold'])
        amount_bought = Decimal(request.POST['amount_bought'])
        rate = Decimal(request.POST['rate'])

        try:
            customer = Customer.objects.get(user_id=customer_id)
        except Customer.DoesNotExist:
            messages.error(request, "Customer not found. Please log in again.")
            return redirect('login')
        wallet = Wallet.objects.get(customer=customer)

        # Update wallet balances
        setattr(wallet, f'balance_{sell_currency.lower()}', getattr(wallet, f'balance_{sell_currency.lower()}') - amount_sold)
        setattr(wallet, f'balance_{buy_currency.lower()}', getattr(wallet, f'balance_{buy_currency.lower()}') + amount_bought)
        wallet.save()

        # Create and save the CurrencyExchange record now
        currency_exchange = CurrencyExchange(
            customer=customer,
            sell_currency=sell_currency,
            buy_currency=buy_currency,
            amount_sold=amount_sold,
            amount_bought=amount_bought,
            rate=rate,
        )
        currency_exchange.save()

        messages.success(request, "Currency exchange successful!")
        return redirect('profile')
    return redirect('exchange_currency')

def get_wallet_balance(request):
    if request.method == "GET":
        customer_id = request.session.get('customer_id')
        try:
            customer = Customer.objects.get(user_id=customer_id)
            wallet = Wallet.objects.get(customer=customer)

            # Get sell and buy currency from GET parameters
            sell_currency = request.GET.get('sell_currency')
            buy_currency = request.GET.get('buy_currency')

            # Get wallet balances for selected currencies
            sell_balance = getattr(wallet, f"balance_{sell_currency.lower()}", 0)
            buy_balance = getattr(wallet, f"balance_{buy_currency.lower()}", 0)

            return JsonResponse({
                'sell_balance': sell_balance,
                'buy_balance': buy_balance,
            })

        except (Customer.DoesNotExist, Wallet.DoesNotExist):
            return JsonResponse({'error': 'Wallet not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# @cache_control(no_cache=True, no_store=True, must_revalidate=True)
def logout(request):
    auth_logout(request)  # Log out the user
    request.session.flush()  # Clear all session data
    
    # Invalidate all user sessions for extra security
    Session.objects.filter(session_key=request.session.session_key).delete()
    
    response = redirect('login')
    response.delete_cookie('sessionid')
    return response
