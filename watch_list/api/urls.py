from django.urls import path, include
#from .views import movie_list, get_movie
from .views import MovieById, MovieListAll

urlpatterns = [
    path("all/", MovieListAll.as_view(), name="list"),
    path("<int:pk>", MovieById.as_view(), name="single"),
]
