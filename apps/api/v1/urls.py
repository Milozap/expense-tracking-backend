from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.categories.views import CategoryViewSet
from apps.transactions.views import TransactionViewSet
from apps.users.views import UserRegistrationView

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/register", UserRegistrationView.as_view(), name="user-register"),
]
