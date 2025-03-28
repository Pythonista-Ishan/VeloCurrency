from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from .models import Beneficiary
from customer.models import Customer
from django.utils.cache import patch_cache_control
from django.views.decorators.cache import cache_control
from django.core.cache import cache

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def register_beneficiary(request):
    customer_id = request.session.get('customer_id')

    # Check if the customer exists
    try:
        customer = Customer.objects.get(user_id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found. Please log in again.")
        return redirect('login')

    if request.method == 'POST':
        # Get form data
        account_name = request.POST.get('account_name', 'NOT AVAILABLE')
        bank_name = request.POST.get('bank_name', 'NOT AVAILABLE')
        bank_address = request.POST.get('bank_address', 'NOT AVAILABLE')
        iban = request.POST.get('iban', 'NOT AVAILABLE')
        sortcode = request.POST.get('sortcode', 'NOT AVAILABLE')
        clearing_code = request.POST.get('clearing_code', 'NOT AVAILABLE')
        bic_code = request.POST.get('bic_code', 'NOT AVAILABLE')
        account_number = request.POST.get('account_number', 'NOT AVAILABLE')
        ifsc = request.POST.get('ifsc', 'NOT AVAILABLE')

        # Save beneficiary
        Beneficiary.objects.create(
            customer=customer,
            account_name=account_name,
            bank_name=bank_name,
            bank_address=bank_address,
            iban=iban,
            sort_code=sortcode,
            clearing_code=clearing_code,
            bic_code=bic_code,
            account_number=account_number,
            ifsc=ifsc,
        )
        messages.success(request, "Beneficiary added successfully!")
        return redirect('register_beneficiary')
    return render(request, 'beneficiary/register_beneficiary.html')

    # Display existing beneficiaries
    # beneficiaries = Beneficiary.objects.filter(customer=customer)
    # return render(request, 'beneficiary/register_beneficiary.html', {'beneficiaries': beneficiaries})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def view_beneficiaries(request):
    customer_id = request.session.get('customer_id')

    # Check if the customer exists
    try:
        customer = Customer.objects.get(user_id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found. Please log in again.")
        return redirect('login')

    # Fetch all beneficiaries for the customer
    beneficiaries = Beneficiary.objects.filter(customer=customer)
    return render(request, 'beneficiary/view_beneficiaries.html', {'beneficiaries': beneficiaries})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def edit_beneficiary(request, beneficiary_id):
    # Ensure the user is logged in and identify the customer
    customer_id = request.session.get('customer_id')
    try:
        customer = Customer.objects.get(user_id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found. Please log in again.")
        return redirect('login')

    # Fetch the beneficiary to edit
    beneficiary = get_object_or_404(Beneficiary, id=beneficiary_id, customer=customer)

    if request.method == 'POST':
        # Get form data and update the beneficiary
        beneficiary.account_name = request.POST.get('account_name', 'NOT AVAILABLE')
        beneficiary.bank_name = request.POST.get('bank_name', 'NOT AVAILABLE')
        beneficiary.bank_address = request.POST.get('bank_address', 'NOT AVAILABLE')
        beneficiary.iban = request.POST.get('iban', 'NOT AVAILABLE')
        beneficiary.sort_code = request.POST.get('sortcode', 'NOT AVAILABLE')
        beneficiary.clearing_code = request.POST.get('clearing_code', 'NOT AVAILABLE')
        beneficiary.bic_code = request.POST.get('bic_code', 'NOT AVAILABLE')
        beneficiary.account_number = request.POST.get('account_number', 'NOT AVAILABLE')
        beneficiary.ifsc = request.POST.get('ifsc', 'NOT AVAILABLE')

        # Save the updated details
        beneficiary.save()
        messages.success(request, "Beneficiary details updated successfully!")
        return redirect('register_beneficiary')

    # Render the edit form with existing details
    context = {
        'beneficiary': beneficiary
    }
    return render(request, 'beneficiary/edit_beneficiary.html', context)