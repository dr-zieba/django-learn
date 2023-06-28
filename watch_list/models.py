from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


# Create your models here.
class Platform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=50)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=15)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey(
        Platform,
        null=True,
        on_delete=models.SET_NULL,
        related_name="watchlist_platform",
    )
    avg_rating = models.FloatField(default=0)
    number_of_rates = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author", null=True
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(
        WatchList, on_delete=models.CASCADE, related_name="watchlist_review"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating)
