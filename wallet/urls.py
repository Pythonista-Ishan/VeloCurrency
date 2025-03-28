from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.wallet_dashboard, name='wallet_dashboard'),
]
