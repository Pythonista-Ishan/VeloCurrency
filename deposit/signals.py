# deposit/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DepositRequest
from wallet.models import Wallet

@receiver(post_save, sender=DepositRequest)
def update_wallet_balance_on_approval(sender, instance, created, **kwargs):
    # Proceed only if the deposit is approved and wasn't just created
    if instance.approved and not created:
        # Get the customer’s wallet
        wallet = Wallet.objects.get(customer=instance.customer)

        # Update the wallet balance based on the currency of the deposit
        if instance.currency == 'GBP':
            wallet.balance_gbp += instance.amount
        elif instance.currency == 'EUR':
            wallet.balance_eur += instance.amount
        elif instance.currency == 'USD':
            wallet.balance_usd += instance.amount
        elif instance.currency == 'INR':
            wallet.balance_inr += instance.amount
        
        # Save the updated wallet balance
        wallet.save()
