# Customers/models.py

from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin

class Customer(models.Model):
    user_id = models.CharField(max_length=10, unique=True, blank=True, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  # Store hashed password

    def save(self, *args, **kwargs):
        # Generate a unique user ID in the format "SCUXXXXX"
        if not self.user_id:
            self.user_id = 'SCU' + str(Customer.objects.count() + 1).zfill(5)
        
        # Only hash the password if it's not already hashed
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

# Signal to generate a unique user ID after saving the instance
@receiver(post_save, sender=Customer)
def create_user_id(sender, instance, created, **kwargs):
    if created and not instance.user_id:
        # Generate a unique user ID in the format "SCUXXXXX"
        instance.user_id = 'SCU' + str(Customer.objects.count()).zfill(5)
        instance.save()

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'email', 'phone_number')
    search_fields = ('name', 'email')

admin.site.register(Customer, CustomerAdmin)