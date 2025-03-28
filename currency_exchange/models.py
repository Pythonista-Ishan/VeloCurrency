# currency_exchange/models.py

from django.db import models
from customer.models import Customer
from django.contrib import admin
import uuid
#from .models import CurrencyExchange

class CurrencyExchange(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sell_currency = models.CharField(max_length=3)  # e.g., 'GBP'
    buy_currency = models.CharField(max_length=3)  # e.g., 'EUR'
    amount_sold = models.DecimalField(max_digits=10, decimal_places=2)
    amount_bought = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        # Generate a unique order ID in the format "Fx1OXXXX"
        if not self.order_id:
            while True:
                potential_order_id = 'Fx1O' + str(uuid.uuid4().int)[:4]
                if not CurrencyExchange.objects.filter(order_id=potential_order_id).exists():
                    self.order_id = potential_order_id
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Exchange Order {self.order_id} by {self.customer.name}"

class CurrencyExchangeAdmin(admin.ModelAdmin):
    list_display = ('customer', 'sell_currency', 'buy_currency', 'amount_sold', 'amount_bought', 'rate', 'timestamp')
    search_fields = ('customer__name', 'sell_currency', 'buy_currency', 'order_id')

admin.site.register(CurrencyExchange, CurrencyExchangeAdmin)