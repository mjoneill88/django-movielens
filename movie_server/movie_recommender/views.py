from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Avg
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.models import User
from .models import Movie, Rater, Rating
from .forms import RaterForm, RatingForm


def index(request):
    average_list = []
    for movie in Movie.objects.all():
        movie_ratings = Rating.objects.filter(movie_id=movie.id)
        if movie_ratings.count() > 10:
            movie_average = movie_ratings.aggregate(Avg('rating'))
            average_list.append((movie_average['rating__avg'], movie.movie_id))
    descending_average_ratings = sorted(average_list, reverse=True)
    top_20_movies = descending_average_ratings[:20]
    template = loader.get_template('movie_recommender/index.html')
    context = {'top_20_movies': top_20_movies}
    return HttpResponse(template.render(context, request))


def movie(request, movie_id):
    movie = Movie.objects.get(movie_id=movie_id)
    rating_list = Rating.objects.filter(movie_id=movie.id)
    rater_queries = rating_list.values_list('user_id', flat=True)
    movie_average = Rating.objects.filter(movie_id=movie.id).aggregate(Avg('rating'))
    template = loader.get_template('movie_recommender/movie.html')
    context = {'movie': movie,
               'rating_list': rating_list,
               'average': movie_average['rating__avg'],
               'rater_queries': rater_queries}
    return HttpResponse(template.render(context, request))


def user(request, user_id):
    rater = Rater.objects.get(rater_id=user_id)
    rating_list = Rating.objects.filter(user_id=rater.id)
    template = loader.get_template('movie_recommender/user.html')
    context = {'rater': rater,
               'rating_list': rating_list}
    return HttpResponse(template.render(context, request))


def register(request):
    new_id = Rater.objects.last().rater_id + 1
    if request.method == 'POST':
        form = RaterForm(request.POST)

        if form.is_valid():
            new_rater = form.save(commit=False)
            new_rater.rater_id = new_id
            user = User.objects.create_user('rater{}'.format(new_id),
                                            'rater{}@here.com'.format(new_id),
                                            'rater{}password'.format(new_id))
            user.save()
            new_rater.user = user
            new_rater.save()
            return user_redirect(request)
        else:
            print(form.errors)
    else:
        form = RaterForm()
    return render(request, 'registration/register.html', {'form': form})


def user_redirect(request):
    url = '/movie_recommender/user{}/'.format(request.user.rater.rater_id)
    return HttpResponseRedirect(url)


def movie_redirect(request, movie_id):
    url = '/movie_recommender/movie{}/'.format(movie_id)
    return HttpResponseRedirect(url)


def rate_movie(request, movie_id):
    if request.method == 'POST':
        form = RatingForm(request.POST)

        if form.is_valid():
            rating = form.save(commit=False)
            rating.movie_id = Movie.objects.get(movie_id=movie_id)
            rating.user_id = Rater.objects.get(rater_id=request.user.rater.rater_id)
            rating.save()
            return movie_redirect(request, movie_id)
        else:
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = RatingForm()
    movie_average = Rating.objects.filter(movie_id=movie_id).aggregate(Avg('rating'))
    context = {'form': form,
               'movie': Movie.objects.get(movie_id=movie_id),
               'movie_average': movie_average['rating__avg']}
    return render(request, 'movie_recommender/rate_movie.html', context)
