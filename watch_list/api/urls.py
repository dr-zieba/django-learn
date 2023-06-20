from django.urls import path, include

# from .views import movie_list, get_movie
from .views import WatchListAll, WatchListById, PlatformAll, PlatformById

urlpatterns = [
    path("watchlist/", WatchListAll.as_view(), name="watchlist"),
    path("watchlist/<int:pk>", WatchListById.as_view(), name="watchlist-detail"),
    path("platform/", PlatformAll.as_view(), name="platform-all"),
    path("platform/<int:pk>", PlatformById.as_view(), name="platform-detail"),
]
