from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Transaction


class AuthRequiredTests(TestCase):
    def test_dashboard_redirects_anonymous_to_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)


class TransactionModelTests(TestCase):
    def test_signed_amount(self):
        income = Transaction(type=Transaction.INCOME, amount=Decimal("100"))
        expense = Transaction(type=Transaction.EXPENSE, amount=Decimal("40"))
        self.assertEqual(income.signed_amount, Decimal("100"))
        self.assertEqual(expense.signed_amount, Decimal("-40"))


class DashboardViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="tester", password="pw12345")
        self.client.force_login(user)
        Transaction.objects.create(
            type=Transaction.INCOME,
            title="Salary",
            amount=Decimal("1000"),
            category="salary",
            date=date.today(),
        )
        Transaction.objects.create(
            type=Transaction.EXPENSE,
            title="Groceries",
            amount=Decimal("250.50"),
            category="food",
            date=date.today(),
        )

    def test_dashboard_shows_balance(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["income"], Decimal("1000"))
        self.assertEqual(response.context["expense"], Decimal("250.50"))
        self.assertEqual(response.context["balance"], Decimal("749.50"))


class TransactionCrudTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="tester", password="pw12345")
        self.client.force_login(user)

    def test_create_transaction(self):
        response = self.client.post(
            reverse("transaction_create"),
            {
                "type": "expense",
                "title": "Coffee",
                "amount": "4.50",
                "category": "food",
                "date": date.today().isoformat(),
                "note": "",
            },
        )
        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(Transaction.objects.count(), 1)

    def test_create_rejects_non_positive_amount(self):
        response = self.client.post(
            reverse("transaction_create"),
            {
                "type": "expense",
                "title": "Bad",
                "amount": "0",
                "category": "food",
                "date": date.today().isoformat(),
                "note": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_delete_transaction(self):
        t = Transaction.objects.create(
            type=Transaction.EXPENSE,
            title="Book",
            amount=Decimal("12"),
            category="other",
            date=date.today(),
        )
        response = self.client.post(reverse("transaction_delete", args=[t.pk]))
        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(Transaction.objects.count(), 0)
