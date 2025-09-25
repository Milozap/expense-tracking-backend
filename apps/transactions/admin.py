from django.contrib import admin

from apps.transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "amount", "category", "date", "description", "admin_color"]
    list_filter = ["category", "date", "category__type"]
    search_fields = ["type", "description"]
