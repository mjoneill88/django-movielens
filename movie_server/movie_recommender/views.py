from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Avg
from django.shortcuts import render
from django.template import loader, RequestContext
from .models import Movie, Rater, Rating
from .forms import RaterForm


def index(request):
    average_list = []
    for movie in Movie.objects.all():
        movie_average = Rating.objects.filter(movie_id=movie.id).aggregate(Avg('rating'))
        average_list.append((movie_average['rating__avg'], movie.movie_id))
    descending_average_ratings = sorted(average_list, reverse=True)
    top_20_movies = descending_average_ratings[:20]
    template = loader.get_template('movie_recommender/index.html')
    context = {'top_20_movies': top_20_movies}
    return HttpResponse(template.render(context, request))

def movie(request, movie_id):
    movie = Movie.objects.get(movie_id=movie_id)
    rating_list = Rating.objects.filter(movie_id=movie.id)
    movie_average = Rating.objects.filter(movie_id=movie.id).aggregate(Avg('rating'))
    template = loader.get_template('movie_recommender/movie.html')
    context = {'movie': movie,
               'rating_list': rating_list,
               'average': movie_average['rating__avg']}
    return HttpResponse(template.render(context, request))

def user(request, user_id):
    rater = Rater.objects.get(rater_id=user_id)
    rating_list = Rating.objects.filter(user_id=rater.id)
    template = loader.get_template('movie_recommender/user.html')
    context = {'rater': rater,
               'rating_list': rating_list}
    return HttpResponse(template.render(context, request))


def register(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = RaterForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = RaterForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).

    # , context_instance=context


def redirect(request):
    url = '/movie_recommender/user{}/'.format(request.user.rater.rater_id)
    return HttpResponseRedirect(url)


def rate_movie(request, movie_id):
    context = RequestContext(request)

    if request.method == 'POST':
        form = RaterForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = RaterForm()
    return render('registration/register.html', {'form': form})
    
