from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_beneficiary, name='register_beneficiary'),
    path('view/', views.view_beneficiaries, name='view_beneficiaries'),
    path('edit/<int:beneficiary_id>/', views.edit_beneficiary, name='edit_beneficiary'),
]
