from django import forms

from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["type", "title", "amount", "category", "date", "note"]
        widgets = {
            "type": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g. Groceries"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "0"}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "note": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "Optional"}
            ),
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount
