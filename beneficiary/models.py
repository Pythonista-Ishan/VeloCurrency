from django.db import models
from customer.models import Customer

class Beneficiary(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Link beneficiary to customer
    account_name = models.CharField(max_length=255, default="NOT AVAILABLE")
    bank_name = models.CharField(max_length=255, default="NOT AVAILABLE")
    bank_address = models.TextField(default="NOT AVAILABLE")
    iban = models.CharField(max_length=34, default="NOT AVAILABLE")
    sort_code = models.CharField(max_length=10, default="NOT AVAILABLE")
    clearing_code = models.CharField(max_length=20, default="NOT AVAILABLE")
    bic_code = models.CharField(max_length=11, default="NOT AVAILABLE")
    account_number = models.CharField(max_length=20, default="NOT AVAILABLE")
    ifsc = models.CharField(max_length=11, default="NOT AVAILABLE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_name} ({self.bank_name})"
