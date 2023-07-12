from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegisterUserTest(APITestCase):
    def test_registration_of_user(self):
        """
        Test creation of a new user
        """
        url = reverse("register")
        data = {
            "username": "testcase_user",
            "email": "test@user.com",
            "password": "password1",
            "password2": "password1",
        }
        response = self.client.post(url, data, format="json")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(User.objects.count(), 1)
        self.assertEquals(User.objects.get().username, "testcase_user")


class LoginLogoutTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testcase_user", password="testcase"
        )

    def test_login_user(self):
        url = reverse("login")
        data = {"username": "testcase_user", "password": "testcase"}
        response = self.client.post(url, data, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        url = reverse("logout")
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
