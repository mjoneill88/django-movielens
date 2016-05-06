from django.db import models


class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=200)

    def __str__(self):
        return "{}: {}".format(self.movie_id, self.title)


class Rater(models.Model):
    user_id = models.IntegerField()
    age = models.IntegerField()
    sex = models.CharField(max_length=1)
    occupation = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        return "Rater ID: {}".format(self.user_id)


class Rating(models.Model):
    user_id = models.ForeignKey(Rater, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return "{}: {}\nUser {} : Rating {}".format(self.movie_id.movie_id,
                                                    self.movie_id.title,
                                                    self.user_id.user_id,
                                                    self.rating)
# Create your models here.
