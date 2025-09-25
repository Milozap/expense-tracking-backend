from django.contrib.auth.models import User
from django.db import models

from apps.categories.models import Category


class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user_id} - {self.description} - {self.amount}"

    def type(self) -> str:
        return self.category.type

    def admin_color(self) -> str:
        return self.category.admin_color()
