from django.db import models


class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=200)
    


class Rater(models.Model):
    user_id = models.IntegerField()
    age = models.IntegerField()
    sex = models.CharField(max_length=1)
    occupation = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=5)


class Rating(models.Model):
    user_id = models.ForeignKey(Rater, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()

# Create your models here.
