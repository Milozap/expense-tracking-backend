from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
        )
        extra_kwargs = {"email": {"required": True}}

    def validate_email(self, data: str) -> str:
        data = data.lower()
        if User.objects.filter(email__iexact=data).exists():
            raise serializers.ValidationError("User with this email already exists")
        return data

    def validate_username(self, value: str) -> str:
        reserved = ["admin", "root", "system", "api", "www"]
        if value.lower() in reserved:
            raise serializers.ValidationError("This username is reserved")
        return value

    def validate(self, data: dict) -> dict:
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError({"password": "Passwords don't match"})

        password = data.get("password")
        if password:
            try:
                password_validation.validate_password(password)
            except ValidationError as e:
                raise serializers.ValidationError({"password": list(e.messages)})

        return data

    def create(self, validated_data: dict) -> User:
        validated_data.pop("password_confirm")

        return User.objects.create_user(**validated_data)
