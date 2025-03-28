from django.urls import path
from . import views

urlpatterns = [
    path('exchange/', views.exchange_currency, name='exchange_currency'),
    path('confirm_exchange/', views.confirm_exchange, name='confirm_exchange'),
    path('get-wallet-balance/', views.get_wallet_balance, name='get_wallet_balance'),
    path('logout/', views.logout, name='logout'),
]
