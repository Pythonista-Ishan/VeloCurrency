from django.db.models.signals import post_save
from django.dispatch import receiver
from customer.models import Customer
from .models import Wallet

@receiver(post_save, sender=Customer)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        # Create a wallet for the new customer with default balances
        Wallet.objects.create(customer=instance)
