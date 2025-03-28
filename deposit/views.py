# deposit/views.py
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import DepositRequest
from customer.models import Customer
from admin_panel.models import AdminSettings  # Adjust the import as needed
from django.contrib import messages

def deposit(request, currency):
    # Check if the customer is logged in and retrieve customer_id
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')

    # Get the customer and ensure the customer exists
    customer = get_object_or_404(Customer, user_id=customer_id)
    
    # Get admin settings to retrieve bank details based on currency
    admin_settings = AdminSettings.objects.first()
    
    # Map currency to the respective bank detail field
    currency_bank_field = f'bank_details_{currency.lower()}'  # e.g., bank_details_gbp for GBP
    bank_details = getattr(admin_settings, currency_bank_field, None)

    # Parse the JSON data if it exists
    if isinstance(bank_details, str):
        bank_details = json.loads(bank_details)
    elif isinstance(bank_details, dict):
        bank_details = bank_details
    else:
        return HttpResponse(f"No bank details available for {currency}", status=404)

    # Check if bank details are available for the selected currency
    if not bank_details:
        return HttpResponse(f"No bank details available for {currency}", status=404)
    
    # If POST request, process deposit (for now, just display the bank details)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        reference_number = request.POST.get('reference_number')
        
        # Create a deposit request if amount and reference number are provided
        if amount and reference_number:
            deposit_request = DepositRequest.objects.create(
                customer=customer,
                currency=currency,
                amount=amount,
                reference_number=reference_number
            )
            messages.success(request, "Deposit request submitted successfully!")
        else:
            messages.error(request, "Please provide both amount and reference number.")

        return redirect('deposit', currency=currency)

    # Render deposit form with bank details
    return render(request, 'deposit/deposit_form.html', {
        'customer': customer,
        'currency': currency,
        'bank_details': bank_details,
    })
