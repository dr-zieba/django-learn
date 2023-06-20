from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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

    def __str__(self):
        return self.title


class Review(models.Model):
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
