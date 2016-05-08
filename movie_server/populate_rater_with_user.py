from movie_recommender.models import Rater
from django.contrib.auth.models import User
for one_rater in Rater.objects.all():
    one_user = User.objects.get(username='rater{}'.format(one_rater.rater_id))
    one_rater.user = one_user
    one_rater.save()
