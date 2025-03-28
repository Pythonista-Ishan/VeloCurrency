# admin_panel/models.py

from django.db import models
from customer.models import Customer
from django.contrib import admin
#from .models import AdminSettings

class AdminSettings(models.Model):
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # Bank account details for deposits
    bank_details_gbp = models.JSONField(blank=True, null=True)
    bank_details_eur = models.JSONField(blank=True, null=True)
    bank_details_usd = models.JSONField(blank=True, null=True)
    bank_details_inr = models.JSONField(blank=True, null=True)

    def __str__(self):
        return "Admin Settings"

class AdminSettingsAdmin(admin.ModelAdmin):
    list_display = ('profit_margin',)
    search_fields = ('profit_margin',)

admin.site.register(AdminSettings, AdminSettingsAdmin)