from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from beneficiary.models import Beneficiary
from .models import Payment
from wallet.models import Wallet
from decimal import Decimal
from customer.models import Customer
from django.utils.cache import patch_cache_control
from django.views.decorators.cache import cache_control
from django.core.cache import cache

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def create_payment(request):
    customer_id = request.session.get('customer_id')
    try:
        customer = Customer.objects.get(user_id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found. Please log in again.")
        return redirect('login')
    wallet = Wallet.objects.get(customer=customer)
    beneficiaries = Beneficiary.objects.filter(customer=customer)

    if request.method == 'POST':
        selected_currency = request.POST.get('currency')
        selected_beneficiary_id = request.POST.get('beneficiary')
        amount = Decimal(request.POST.get('amount'))

        # Validate wallet balance
        #wallet = wallet.first()
        balance = getattr(wallet, f"balance_{selected_currency.lower()}")
        if balance < amount:
            messages.error(request, "Insufficient balance in the selected wallet.")
            return redirect('create_payment')

        # Redirect to the summary page
        return redirect('payment_summary', currency=selected_currency, beneficiary_id=selected_beneficiary_id, amount=amount)

    return render(request, 'payments/create_payment.html', {'wallets': wallet, 'beneficiaries': beneficiaries})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def payment_summary(request, currency, beneficiary_id, amount):
    customer_id = request.session.get('customer_id')
    try:
        customer = Customer.objects.get(user_id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found. Please log in again.")
        return redirect('login')
    # Fetch beneficiary details
    beneficiary = get_object_or_404(Beneficiary, id=beneficiary_id, customer=customer)

    if request.method == 'POST':
        # Deduct from wallet and create the payment
        wallet = Wallet.objects.get(customer=customer)
        setattr(wallet, f"balance_{currency.lower()}", getattr(wallet, f"balance_{currency.lower()}") - Decimal(amount))
        wallet.save()

        # Create payment record
        payment = Payment.objects.create(
            customer=wallet.customer,
            beneficiary=beneficiary,
            amount=amount,
            currency=currency,
        )

        # Redirect to the payment details page
        return redirect('payment_details', payment_id=payment.id)

    return render(request, 'payments/payment_summary.html', {
        'currency': currency,
        'beneficiary': beneficiary,
        'amount': amount
    })

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def payment_details(request, payment_id):
    customer_id = request.session.get('customer_id')
    try:
        customer = Customer.objects.get(user_id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found. Please log in again.")
        return redirect('login')

    # Fetch payment details
    payment = get_object_or_404(Payment, id=payment_id, customer=customer)

    return render(request, 'payments/payment_details.html', {'payment': payment})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def show_payments(request):
    customer_id = request.session.get('customer_id')
    try:
        customer = Customer.objects.get(user_id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found. Please log in again.")
        return redirect('login')

    # Fetch all payments by the customer
    payments = Payment.objects.filter(customer=customer).order_by('-created_at')
    return render(request, 'payments/show_payments.html', {'payments': payments})

