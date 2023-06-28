from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .views import movie_list, get_movie
from .views import (
    WatchListAll,
    WatchListById,
    PlatformAll,
    ReviewList,
    ReviewDetail,
    ReviewCreate,
)

router = DefaultRouter()
router.register("platform", PlatformAll, basename="platform-all")

urlpatterns = [
    path("watchlist/", WatchListAll.as_view(), name="watchlist"),
    path("<int:pk>", WatchListById.as_view(), name="watchlist-detail"),
    path("", include(router.urls)),
    # path("platform/", PlatformAll.as_view(), name="platform-all"),
    # path("platform/<int:pk>", PlatformById.as_view(), name="platform-detail"),
    path("<int:pk>/review-create", ReviewCreate.as_view(), name="review-create"),
    path("<int:pk>/review", ReviewList.as_view(), name="review-list"),
    path("review/<int:pk>", ReviewDetail.as_view(), name="review-detail"),
]
