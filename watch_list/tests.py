from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json

from .api.serializers import PlatformSerializer
from .models import Platform, WatchList, Review


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

    def test_platform_delete(self):
        url = reverse("platform-detail", args=(self.platform.id,))
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class WatchListTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="test")
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.platform = Platform.objects.create(
            name="Test", about="TestCase", website="http://test.com"
        )
        self.movie = WatchList.objects.create(
            title="test", description="test", platform=self.platform
        )

    def test_watchlist_crete(self):
        url = reverse("watchlist-list")
        data = {"title": "test", "description": "test", "platform": self.platform}
        response = self.client.post(url, data, formt="json")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_get_list(self):
        url = reverse("watchlist-list")
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_watchlist_get_by_id(self):
        url = reverse("watchlist-detail", args=(self.movie.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(WatchList.objects.get().title, "test")


class ReviewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="test")
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.platform = Platform.objects.create(
            name="Test", about="TestCase", website="http://test.com"
        )
        self.movie = WatchList.objects.create(
            title="test", description="test", platform=self.platform
        )
        self.movie2 = WatchList.objects.create(
            title="test2", description="test2", platform=self.platform
        )
        self.review = Review.objects.create(
            user=self.user, rating=5, description="test", watchlist=self.movie2
        )

    def test_review_create(self):
        url = reverse("review-create", args=(self.movie.id,))
        data = {
            "user": self.user.id,
            "rating": 5,
            "description": "test",
            "watchlist": self.movie.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Review.objects.count(), 2)
        self.assertEquals(
            Review.objects.get(id=json.loads(response.content).get("id")).description,
            "test",
        )

        response = self.client.post(url, data, format="json")
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_update(self):
        url = reverse("review-detail", args=(self.review.id,))
        data = {"rating": 3}
        response = self.client.put(url, data, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_review_create_unauth_user(self):
        url = reverse("review-create", args=(self.movie.id,))
        data = {
            "user": self.user.id,
            "rating": 5,
            "description": "test",
            "watchlist": self.movie.id,
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data, format="json")
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_list(self):
        url = reverse("review-list", args=(self.movie.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_review_id(self):
        url = reverse("review-detail", args=(self.movie.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
