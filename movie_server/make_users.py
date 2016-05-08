import django
import os
from movie_recommender.models import Rater
from django.contrib.auth.models import User
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_server.settings')
django.setup()


for rater in Rater.objects.all():
    user = User.objects.create_user('rater{}'.format(rater.rater_id),
                                    'rater{}@here.com'.format(rater.rater_id),
                                    'rater{}password'.format(rater.rater_id))
    user.save()
