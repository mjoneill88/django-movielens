from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count


class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=200)

    def __str__(self):
        return "{}: {}".format(self.movie_id, self.title)

    def get_average_rating(self):
        movie_ratings = Rating.objects.filter(movie_id=self.id)
        movie_average = movie_ratings.aggregate(models.Avg('rating'))
        return movie_average['rating__avg']


class Rater(models.Model):
    sex_choices = (
        ('F', 'F'),
        ('M', 'M')
    )
    rater_id = models.IntegerField()
    age = models.IntegerField()
    sex = models.CharField(max_length=1, choices=sex_choices)
    occupation = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=5)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Rater ID: {}".format(self.user_id)


class Rating(models.Model):
    rating_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    user_id = models.ForeignKey(Rater, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=rating_choices)

    def __str__(self):
        return "Movie {}: {}\nUser {} : Rating {}".format(
            self.movie_id.movie_id,
            self.movie_id.title,
            self.user_id.user_id,
            self.rating)

    @staticmethod
    def get_top_rated_movies(ratings_set, number_of_movies):
        pop_movies = ratings_set.annotate(
            count=Count('movie_id')).filter(count__gt=9)
        sorted_movies = pop_movies.values('movie_id').annotate(
            avg_rating=Avg('rating')).order_by('-avg_rating')
        tuple_list = [(x['movie_id'], x['avg_rating']) for x in sorted_movies]
        return tuple_list[:number_of_movies]
