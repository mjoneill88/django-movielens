import pandas as pd
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_server.settings')
django.setup()
from movie_recommender.models import Movie, Rater, Rating

nineteen_genres = ['Genre {}'.format(x) for x in range(19)]
movies = pd.read_csv('u.item', encoding='latin_1', delimiter='|', index_col=False, header=None, names=['movie_id', 'movie_title', 'date', 'URL']+nineteen_genres)
for row in movies.iterrows():
    movie_dict = row[1].to_dict()
    flick_object = Movie(movie_id = movie_dict['movie_id'],
    title = movie_dict['movie_title'])
    flick_object.save()

user_columns = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
imported_user = pd.read_csv('u.user', delimiter='|', header=None, index_col=False, names=user_columns)
for row in imported_user.iterrows():
    user_dict = row[1].to_dict()
    user_object = Rater(user_id=user_dict['user_id'],
                        age=user_dict['age'],
                        sex=user_dict['sex'],
                        occupation=user_dict['occupation'],
                        zip_code=user_dict['zip_code'])
    user_object.save()

data_columns = ['user_id', 'movie_id', 'rating', 'timestamp']
imported_data = pd.read_csv('u.data', delimiter='\t', header=None, index_col=False, names=data_columns)
for row in imported_data.iterrows():
    rating_dict = row[1].to_dict()
    movie = Movie.objects.get(movie_id=rating_dict['movie_id'])
    rater = Rater.objects.get(user_id=rating_dict['user_id'])
    rating_object = Rating(user_id=rater, movie_id=movie, rating=rating_dict['rating'])
    rating_object.save()












# ciw =[0,3,4,6,16, 24]
# summary_activity = pd.read_csv('/Users/mjoneill/Documents/week4/wasting-time/data/atussum_2014.dat', usecols = ciw)
# summary_activity.head()
#
# summary_activity.columns=['ID','Age','Sex','Race','WeeklyEarn','Time Slept']
#
#
# data_list=[]
# with open('u.data', 'r', encoding='latin_1') as item_file:
#     reader_data=csv.DictReader(item_file, delimiter='\t', fieldnames=[ 'user_id', 'movie_id', 'rating', 'timestamp'])#expects header
#     for el in reader_data:
#         data_list.append(el)
#
#
# >>> import csv
# >>> with open('eggs.csv', newline='') as csvfile:
# ...     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
# ...     for row in spamreader:
