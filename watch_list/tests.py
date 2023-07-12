from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json

from .api.serializers import PlatformSerializer
from .models import Platform


class PlatformTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testcase_user", password="testcase"
        )
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # self.super_user = User.objects.create_superuser(username='test_superuser', password='testsuper')
        # self.token_super = Token.objects.get(user__username=self.super_user.username)
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_super.key)

        self.platform = Platform.objects.create(
            name="Test", about="TestCase", website="http://test.com"
        )

    def test_platform_create(self):
        url = reverse("platform-list")
        data = {"name": "testPltform", "about": "test", "website": "http://test.com"}
        response = self.client.post(url, data, format="json")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_platform_get_list(self):
        url = reverse("platform-list")
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_platform_get_one_elem(self):
        url = reverse("platform-detail", args=(self.platform.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
