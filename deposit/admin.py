# deposit/admin.py
from django.contrib import admin
from .models import DepositRequest
from wallet.models import Wallet

def approve_deposit(modeladmin, request, queryset):
    for deposit in queryset:
        if not deposit.approved:
            deposit.approved = True
            deposit.save()  # This will trigger the post_save signal to update the wallet balance

approve_deposit.short_description = "Approve selected deposits"

@admin.register(DepositRequest)
class DepositRequestAdmin(admin.ModelAdmin):
    list_display = ('customer', 'currency', 'amount', 'approved', 'created_at')
    actions = [approve_deposit]
