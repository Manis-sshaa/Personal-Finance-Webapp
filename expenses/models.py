from django.db import models


class Transaction(models.Model):
    """A single money movement: either income or an expense."""

    INCOME = "income"
    EXPENSE = "expense"
    TYPE_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]

    CATEGORY_CHOICES = [
        ("food", "Food & Groceries"),
        ("transport", "Transport"),
        ("housing", "Housing & Bills"),
        ("shopping", "Shopping"),
        ("health", "Health"),
        ("entertainment", "Entertainment"),
        ("salary", "Salary"),
        ("other", "Other"),
    ]

    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default=EXPENSE)
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    date = models.DateField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.get_type_display()}: {self.title} ({self.amount})"

    @property
    def signed_amount(self):
        """Positive for income, negative for expense."""
        if self.type == self.EXPENSE:
            return -self.amount
        return self.amount
