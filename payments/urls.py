from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pay/', views.payment_form, name='payment_form'),
    path('status/<str:transaction_id>/', views.payment_status, name='payment_status'),
]
