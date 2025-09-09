from rest_framework import filters, permissions, viewsets

from apps.api.v1.serializers import CategorySerializer
from apps.categories.models import Category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.select_related("parent")
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "slug"]
