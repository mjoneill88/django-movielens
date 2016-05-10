from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Avg, Count
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Movie, Rater, Rating
from .forms import RaterForm, RatingForm


def index(request):
    all_ratings = Rating.objects.all()
    top_20_movies = Rating.get_top_rated_movies(all_ratings, 20)
    context = {'top_20_movies': top_20_movies}
    return render(request, 'movie_recommender/index.html', context)


def movie(request, movie_id):
    movie = Movie.objects.get(movie_id=movie_id)
    rating_list = Rating.objects.filter(movie_id=movie.id)
    rater_queries = rating_list.values_list('user_id', flat=True)
    movie_average = movie.get_average_rating
    context = {'movie': movie,
               'rating_list': rating_list,
               'average': movie_average,
               'rater_queries': rater_queries}
    return render(request, 'movie_recommender/movie.html', context)


def user(request, user_id):
    rater = Rater.objects.get(rater_id=user_id)
    rating_list = Rating.objects.filter(user_id=rater.id)
    page_user = User.objects.get(username='rater{}'.format(user_id))
    if request.user == page_user:
        seen_movies = rating_list.values_list(
            'movie_id', flat=True)
        unseen_ratings = Rating.objects.exclude(movie_id__in=seen_movies)
        top_20_movies = Rating.get_top_rated_movies(unseen_ratings, 20)
        context = {'top_20_movies': top_20_movies,
                   'rating_list': rating_list,
                   'rater': rater}
    else:
        context = {'rater': rater,
                   'rating_list': rating_list}
    return render(request, 'movie_recommender/user.html', context)


def register(request):
    new_id = Rater.objects.last().rater_id + 1
    if request.method == 'POST':
        form = RaterForm(request.POST)

        if form.is_valid():
            new_rater = form.save(commit=False)
            new_rater.rater_id = new_id
            new_user = User.objects.create_user('rater{}'.format(new_id),
                                                'rater{}@here.com'.format(new_id),
                                                'rater{}password'.format(new_id))
            new_user.save()
            new_rater.user = new_user
            new_rater.save()
            user = authenticate(username=new_user.username, password='rater{}password'.format(new_id))
            if user is not None:
                if user.is_active:
                    login(request, user)
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
