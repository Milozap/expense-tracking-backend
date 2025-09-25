from rest_framework import filters, permissions, viewsets

from apps.transactions.models import Transaction
from apps.transactions.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["description", "type", "user__username"]
