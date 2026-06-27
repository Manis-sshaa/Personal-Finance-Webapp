from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "type", "title", "category", "amount")
    list_filter = ("type", "category", "date")
    search_fields = ("title", "note")
    date_hierarchy = "date"
