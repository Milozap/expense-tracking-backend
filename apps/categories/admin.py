from django.contrib import admin

from apps.categories.models import Category


class CategoryAdmin(admin.ModelAdmin):

    list_display = ("type", "name", "admin_color", "parent")
    list_filter = ("type",)
    search_fields = ("name", "slug")


admin.site.register(Category, CategoryAdmin)
