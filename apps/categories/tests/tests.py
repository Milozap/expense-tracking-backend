import pytest
from django.urls import reverse

from ..models import Category
from .factories import CategoryFactory


@pytest.mark.django_db
class TestCategoryCRUD:
    def test_retrieve_categories(self, api_client) -> None:
        CategoryFactory.create_batch(5)
        response = api_client.get(reverse("category-list"))
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_can_not_delete_category(self, api_client) -> None:
        category = CategoryFactory.create()
        response = api_client.delete(
            reverse("category-detail", kwargs={"pk": category.pk})
        )
        assert response.status_code == 405
        assert Category.objects.filter(pk=category.pk).exists()

    def test_can_not_update_category(self, api_client) -> None:
        category = CategoryFactory.create()
        update_data = {"name": "Updated Name", "type": "INCOME"}
        response = api_client.put(
            reverse("category-detail", kwargs={"pk": category.pk}), data=update_data
        )
        assert response.status_code == 405
