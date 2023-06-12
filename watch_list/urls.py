from django.urls import path, include
from .views import movie_list, get_movie

urlpatterns = [
    path("all/", movie_list, name="list"),
    path("<int:id>", get_movie, name="single"),
]
