from django.urls import path
from . import views

urlpatterns = [
    path('<str:currency>/deposit/', views.deposit, name='deposit'),
]
