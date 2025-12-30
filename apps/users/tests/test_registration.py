import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from .factories import UserFactory


@pytest.mark.django_db
class TestUserRegistration:
    def test_register_with_valid_data_creates_user_and_returns_tokens(
        self, api_client: APIClient
    ) -> None:
        """User successfully registers and receives access and refresh tokens."""
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
        }
        response = api_client.post(reverse("user-register"), data=payload)

        assert response.status_code == 201

        assert User.objects.filter(username="testuser").exists()

        data = response.json()
        assert "access" in data
        assert "refresh" in data
        assert "user" in data
        assert "id" in data["user"]
        assert data["user"]["username"] == "testuser"
        assert data["user"]["email"] == "testuser@example.com"

        assert "password" not in data["user"]
        assert "password_confirm" not in data["user"]
        assert "first_name" not in data["user"]
        assert "last_name" not in data["user"]

    def test_register_with_valid_data_password_is_hashed(
        self, api_client: APIClient
    ) -> None:
        """Password is hashed in database, not stored as plain text."""
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "PlainTextPassword123!",
            "password_confirm": "PlainTextPassword123!",
        }
        api_client.post(reverse("user-register"), data=payload)

        user = User.objects.get(username="testuser")
        # Password should be hashed, not plain text
        assert user.password != "PlainTextPassword123!"
        # Password hash should use Django's hashing format
        assert user.password.startswith(("pbkdf2_sha256$", "md5$", "argon2"))
        # Verify the password is actually correct
        assert user.check_password("PlainTextPassword123!")

    def test_register_without_required_fields_returns_400(
        self, api_client: APIClient
    ) -> None:
        """
        Missing required fields
        (username, email, password, password_confirm) return 400.
        """
        # Missing username
        payload = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 400
        assert "username" in response.json()

        # Missing email
        payload = {
            "username": "testuser",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 400
        assert "email" in response.json()

        # Missing password
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password_confirm": "SecurePass123!",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 400
        assert "password" in response.json()

        # Missing password_confirm
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePass123!",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 400
        assert "password_confirm" in response.json()

    def test_register_with_invalid_email_format_returns_400(
        self, api_client: APIClient
    ) -> None:
        """Invalid email format is rejected."""
        payload = {
            "username": "testuser",
            "email": "not_a_valid_email",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 400
        assert "email" in response.json()

    def test_register_with_password_too_short_returns_400(
        self, api_client: APIClient
    ) -> None:
        """Password shorter than 8 characters is rejected."""
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "short",
            "password_confirm": "short",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 400
        assert "password" in response.json()

    def test_register_with_common_password_returns_400(
        self, api_client: APIClient
    ) -> None:
        """Common passwords are rejected by Django validators."""
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password",
            "password_confirm": "password",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 400
        assert "password" in response.json()

    def test_register_with_numeric_only_password_returns_400(
        self, api_client: APIClient
    ) -> None:
        """All-numeric password is rejected by Django validators."""
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "12345678",
            "password_confirm": "12345678",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 400
        assert "password" in response.json()

    def test_register_with_mismatched_passwords_returns_400(
        self, api_client: APIClient
    ) -> None:
        """Mismatched password and password_confirm are rejected."""
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePass123!",
            "password_confirm": "DifferentPass123!",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 400
        assert "password" in response.json() or "non_field_errors" in response.json()

    def test_register_with_existing_username_returns_400(
        self, api_client: APIClient
    ) -> None:
        """Cannot register with username that already exists."""
        UserFactory(username="existinguser")

        payload = {
            "username": "existinguser",
            "email": "newemail@example.com",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 400
        assert "username" in response.json()

    def test_register_with_existing_email_returns_400_with_explicit_message(
        self, api_client: APIClient
    ) -> None:
        """Cannot register with email that already exists, error message is explicit."""
        UserFactory(email="existing@example.com")

        payload = {
            "username": "newuser",
            "email": "existing@example.com",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 400
        assert "email" in response.json()
        # Error message should be explicit about email existing
        error_message = str(response.json()["email"]).lower()
        assert (
            "exist" in error_message
            or "already" in error_message
            or "registered" in error_message
        )

    def test_register_with_optional_first_name_and_last_name_stored(
        self, api_client: APIClient
    ) -> None:
        """First and last names are optional but stored correctly when provided."""
        # Without names
        payload = {
            "username": "nonames",
            "email": "nonames@example.com",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 201
        user = User.objects.get(username="nonames")
        assert user.first_name == ""
        assert user.last_name == ""

        # With names
        payload = {
            "username": "withnames",
            "email": "withnames@example.com",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        assert response.status_code == 201
        user = User.objects.get(username="withnames")
        assert user.first_name == "John"
        assert user.last_name == "Doe"

    def test_returned_access_token_is_valid_for_authenticated_requests(
        self, api_client: APIClient
    ) -> None:
        """
        Access token returned from registration can authenticate
        subsequent requests.
        """
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
        }
        response = api_client.post(reverse("user-register"), data=payload)
        data = response.json()
        access_token = data["access"]

        # Use the token to make an authenticated request
        # We'll test by calling a protected endpoint (transactions or categories list)
        # which requires authentication
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        protected_response = api_client.get(reverse("transaction-list"))

        # Should not be 401 Unauthorized (token is valid)
        assert protected_response.status_code != 401

    def test_unauthenticated_user_can_register(self, api_client: APIClient) -> None:
        """Registration endpoint allows unauthenticated requests."""
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
        }
        # No authentication header set
        response = api_client.post(reverse("user-register"), data=payload)

        # Should succeed without authentication
        assert response.status_code == 201
        assert User.objects.filter(username="testuser").exists()
