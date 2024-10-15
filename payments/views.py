import uuid
from random import choice
from django.shortcuts import render, redirect
from .models import Transaction
from .forms import PaymentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'payments/dashboard.html', {'transactions': transactions})

@login_required
def payment_form(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction = create_transaction(request.user, amount)
            return redirect('payment_status', transaction_id=transaction.transaction_id)
    else:
        form = PaymentForm()

    return render(request, 'payments/payment_form.html', {'form': form})

@login_required
def payment_status(request, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id, user=request.user)

    # Simulating payment processing and status change
    if transaction.status == 'pending':
        transaction.status = choice(['completed', 'failed'])
        transaction.save()

    return render(request, 'payments/payment_status.html', {'transaction': transaction})

def create_transaction(user, amount):
    transaction_id = str(uuid.uuid4())
    transaction = Transaction.objects.create(
        user=user,
        amount=amount,
        transaction_id=transaction_id,
        status='pending'
    )
    return transaction
