from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        max_length=20, write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        password = self.validated_data.get("password")
        password2 = self.validated_data.get("password2")

        if password != password2:
            raise serializers.ValidationError({"error": "passwords do not match"})

        if User.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "email already exist"})

        if User.objects.filter(username=self.validated_data["username"]).exists():
            raise serializers.ValidationError({"error": "user already exists"})

        account = User(
            email=self.validated_data["email"], username=self.validated_data["username"]
        )
        account.set_password(password)
        account.save()

        return account
