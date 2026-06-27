from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TransactionForm
from .models import Transaction


def _totals():
    aggregates = Transaction.objects.values("type").annotate(total=Sum("amount"))
    income = expense = 0
    for row in aggregates:
        if row["type"] == Transaction.INCOME:
            income = row["total"] or 0
        elif row["type"] == Transaction.EXPENSE:
            expense = row["total"] or 0
    return income, expense, income - expense


@login_required
def dashboard(request):
    income, expense, balance = _totals()
    transactions = Transaction.objects.all()[:10]
    context = {
        "income": income,
        "expense": expense,
        "balance": balance,
        "transactions": transactions,
    }
    return render(request, "expenses/dashboard.html", context)


@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(
        request, "expenses/transaction_list.html", {"transactions": transactions}
    )


@login_required
def transaction_create(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction added.")
            return redirect("dashboard")
    else:
        form = TransactionForm(initial={"date": timezone.now().date()})
    return render(
        request,
        "expenses/transaction_form.html",
        {"form": form, "title": "Add transaction"},
    )


@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated.")
            return redirect("dashboard")
    else:
        form = TransactionForm(instance=transaction)
    return render(
        request,
        "expenses/transaction_form.html",
        {"form": form, "title": "Edit transaction"},
    )


@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        transaction.delete()
        messages.success(request, "Transaction deleted.")
        return redirect("dashboard")
    return render(
        request,
        "expenses/transaction_confirm_delete.html",
        {"transaction": transaction},
    )
