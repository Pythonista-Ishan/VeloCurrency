from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_payment, name='create_payment'),
    path('summary/<str:currency>/<int:beneficiary_id>/<str:amount>/', views.payment_summary, name='payment_summary'),
    path('details/<int:payment_id>/', views.payment_details, name='payment_details'),
    path('list/', views.show_payments, name='show_payments'),
]
