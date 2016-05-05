from django.http import HttpResponse
from django.db.models import Avg
from django.shortcuts import render
from django.template import loader
from .models import Movie, Rater, Rating

def index(request):
    average_list = []
    for movie in Movie.objects.all():
        movie_average = Rating.objects.filter(movie_id=movie.id).aggregate(Avg('rating'))
        average_list.append((movie_average['rating__avg'], movie.id))
    descending_average_ratings = sorted(average_list, reverse=True)
    top_20_movies = descending_average_ratings[:20]
    template = loader.get_template('movie_recommender/index.html')
    context = {'top_20_movies': top_20_movies}
    return HttpResponse(template.render(context, request))


# Create your views here.
