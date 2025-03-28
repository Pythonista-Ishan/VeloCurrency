# wallet/models.py

from django.db import models
from customer.models import Customer
from django.contrib import admin

class Wallet(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    balance_gbp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_eur = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_inr = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.customer.name}'s Wallet"

class WalletAdmin(admin.ModelAdmin):
    list_display = ('customer', 'balance_gbp', 'balance_eur', 'balance_usd', 'balance_inr')
    search_fields = ('customer__name',)

admin.site.register(Wallet, WalletAdmin)