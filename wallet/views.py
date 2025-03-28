from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wallet
from customer.models import Customer

@login_required
def wallet_dashboard(request):
    customer = get_object_or_404(Customer, email=request.user.email)
    wallet = get_object_or_404(Wallet, customer=customer)
    return render(request, 'wallet/wallet_dashboard.html', {'wallet': wallet})
