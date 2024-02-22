from django.shortcuts import render, redirect
from core.models import Transaction
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q


@login_required
def SearchUsersRequest(request):
    account = Account.objects.all()
    query = request.POST.get("account_number")

    if query:
        account = account.filter(
            Q(account_number=query) |
            Q(account_id=query)
        ).distinct()

    context = {
        "account": account,
        "query": query,
    }
    return render(request, "payment_request/search-users.html", context)

# amount reques

def AmountRequest(request, account_number):
    account = Account.objects.get(account_number=account_number)
    context = {
        "account": account
    }
    return render(request, "payment_request/amount-request.html")
