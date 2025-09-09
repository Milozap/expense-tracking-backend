from django.db import models


class Category(models.Model):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TYPE_CHOICES = [(INCOME, "Income"), (EXPENSE, "Expense")]

    name = models.CharField(max_length=64)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, related_name="children"
    )
    slug = models.SlugField(max_length=80, unique=True)
    color = models.CharField(max_length=7, blank=True)

    class Meta:
        unique_together = [("name", "parent", "type")]
        indexes = [models.Index(fields=["type", "parent"])]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name
