from django.shortcuts import render, redirect
from core.models import Transaction
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal


@login_required
def SearchUsersRequest(request):
    account = Account.objects.all()
    query = request.POST.get("account_number")

    if query:
        account = account.filter(
            Q(account_number=query) |
            Q(account_number=query)
        ).distinct()

    context = {
        "account": account,
        "query": query,
    }
    return render(request, "payment_request/search-users.html", context)


def AmountRequest(request, account_number):
    account = Account.objects.get(account_number=account_number)
    context = {
        "account": account
    }
    return render(request, "payment_request/amount-request.html", context)


def AmountRequestProcess(request, account_number):
    account = Account.objects.get(account_number=account_number)

    sender = request.user
    reciever = account.user

    sender_account = request.user.account
    reciever_account = account

    if request.method == "POST":
        amount = request.POST.get("amount-request")
        description = request.POST.get("description")

        new_request = Transaction.objects.create(
            user=request.user,
            amount=amount,
            description=description,

            sender=sender,
            reciever=reciever,

            sender_account=sender_account,
            reciever_account=reciever_account,

            status="request_processing",
            transaction_type="request"
        )
        new_request.save()
        transaction_id = new_request.transaction_id
        return redirect("core:amount-request-confirmation", account.account_number, transaction_id)
    else:
        messages.warning(request, "Error occured, Try again later")
        return redirect("account:dashboard")


def AmountRequestConfirmation(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "account": account,
        "transaction": transaction,
    }
    return render(request, "payment_request/amount-request-confirmation.html", context)


def AmountRequestFinalProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            transaction.status = "request_sent"
            transaction.save()

            messages.success(
                request, "Your payment request has beeen sent successfully.")
            return redirect("core:amount-request-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "An error occured, Try again later.")
            return redirect("account:dashboard")


def RequestCompleted(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "account": account,
        "transaction": transaction,
    }
    return render(request, "payment_request/amount-request-completed.html", context)


def settlement_confirmation(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "account": account,
        "transaction": transaction,
    }
    return render(request, "payment_request/settlement-confirmation.html", context)


def settlement_processing(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    sender = request.user
    sender_account = request.user.account

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            if sender_account.account_balance <= 0 or sender_account.account_balance < transaction.amount:
                messages.warning(
                    request, "Insufficient fund. fund yor account and try again")
            else:
                sender_account.account_balance -= transaction.amount
                sender_account.save()

                account.account_balance += transaction.amount
                account.save()

                transaction.status = "request_settled"
                transaction.save()

                messages.success(
                    request, f"Settled to {account.user.kyc.full_name} was successful")
                return redirect("core:settlement-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "incorrect pin")
            return redirect("core:settlement-confirmation", account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "Error occured")
        return redirect("account:dashboard")


def SettlementCompleted(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "account": account,
        "transaction": transaction,
    }
    return render(request, "payment_request/settlement-completed.html", context)


def deletePaymentRequest(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.user == transaction.user:
        transaction.delete()
        messages.success(request, "Payment request deleted successfully")
        return redirect("core:transactions")

    context = {
        "account": account,
        "transaction": transaction,
    }
    return render(request, "payment_request/delete-payment-request.html", context)
