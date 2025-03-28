"""
URL configuration for VeloCurrency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from customer.views import landing_page



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('customer/', include('customer.urls')),  # Include the Customers app URLs
    path('wallet/', include('wallet.urls')),
    path('deposit/', include('deposit.urls')),
    path('currency_exchange/', include('currency_exchange.urls')),
    path('beneficiary/', include('beneficiary.urls')),
    path('payments/', include('payments.urls')),


]
