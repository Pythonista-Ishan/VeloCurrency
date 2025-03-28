# # Customers/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Customer
# from wallet.models import Wallet

# @receiver(post_save, sender=Customer)
# def create_wallets(sender, instance, created, **kwargs):
#     if created:
#         currencies = ['GBP', 'EUR', 'USD', 'INR']
#         for currency in currencies:
#             Wallet.objects.create(customer=instance, currency=currency, balance=0)
