# deposit/models.py

from django.db import models
from customer.models import Customer
#from .models import DepositRequest

class DepositRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3)  # e.g., 'GBP', 'EUR'
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deposit by {self.customer.name} for {self.amount} {self.currency}"
