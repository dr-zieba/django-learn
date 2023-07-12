from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegistrationSerializer
from rest_framework.authtoken.models import Token

from user_app import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class Registration(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data["username"] = account.username
            data["email"] = account.email

            # Token returned after registration
            # Used with Token auth
            token = Token.objects.get(user=account).key
            data["token"] = token

            # Used with JWT auth
            # refresh = RefreshToken.for_user(account)
            # data["refresh"] = str(refresh)
            # data["access"] = str(refresh.access_token)
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"msg": "Token deleted"}, status=status.HTTP_204_NO_CONTENT)
