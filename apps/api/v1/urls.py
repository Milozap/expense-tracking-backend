from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.categories.views import CategoryViewSet
from apps.transactions.views import TransactionViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = [path("", include(router.urls))]
