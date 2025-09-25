import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import Transaction
from .factories import TransactionFactory


@pytest.mark.django_db
class TestTransactionCRUD:
    def test_retrieve_transactions(self, api_client: APIClient) -> None:
        TransactionFactory.create_batch(5)
        response = api_client.get(reverse("transaction-list"))
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_can_not_delete_transaction(self, api_client: APIClient) -> None:
        transaction = TransactionFactory.create()
        response = api_client.delete(
            reverse("transaction-detail", kwargs={"pk": transaction.pk})
        )
        assert response.status_code == 405
        assert Transaction.objects.filter(pk=transaction.pk).exists()

    def test_can_not_update_transaction(self, api_client: APIClient) -> None:
        transaction = TransactionFactory.create()
        update_data = {
            "date": "2023-01-01",
            "amount": 100.00,
            "description": "Updated Description",
        }
        response = api_client.put(
            reverse("transaction-detail", kwargs={"pk": transaction.pk}),
            data=update_data,
        )
        assert response.status_code == 405
