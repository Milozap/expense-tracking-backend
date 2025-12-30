from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.users.views import UserRegistrationView

router = DefaultRouter()

urlpatterns = [
    path("auth/register", UserRegistrationView.as_view(), name="user-register"),
]
