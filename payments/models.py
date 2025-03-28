from django.db import models
from customer.models import Customer
from beneficiary.models import Beneficiary
from django.contrib import admin
from django.core.exceptions import ValidationError
import uuid


class Payment(models.Model):
    CURRENCY_CHOICES = [
        ('GBP', 'British Pound'),
        ('EUR', 'Euro'),
        ('USD', 'US Dollar'),
        ('INR', 'Indian Rupee'),
    ]

    STATUS_CHOICES = [
        ('Initiated', 'Initiated'),
        ('Remitted', 'Remitted'),
        ('Failed', 'Failed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Initiated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=20, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"PAY1O{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero.")

    def __str__(self):
        return f"Payment {self.order_id} by {self.customer.name}"


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'beneficiary', 'amount', 'currency', 'status', 'created_at')
    search_fields = ('customer__name', 'beneficiary__name', 'currency', 'order_id')
    list_filter = ('status', 'currency', 'created_at')

admin.site.register(Payment, PaymentAdmin)
