from django.shortcuts import render
from .models import Movie
from django.http import JsonResponse


# Create your views here.
def movie_list(request):
    qs = Movie.objects.all()
    context = {"movies": list(qs.values())}
    return JsonResponse(context)


def get_movie(request, id):
    qs = Movie.objects.filter(id=id)
    context = {id: list(qs.values())}
    return JsonResponse(context)
