from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
# Create your views here.

def movie_list(request):
  movies = Movie.objects.all()
  data = {
    'movies' : list(movies.values())
  }
  return JsonResponse(data)
  
def movie_detail(request, pk):
  movie = Movie.objects.get(pk=pk)

  data = {
    'movie' : movie 
  }

  return HttpResponse(movie)