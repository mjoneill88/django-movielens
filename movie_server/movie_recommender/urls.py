from django.conf.urls import url

from . import views

app_name = 'movie_recommender'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^movie(?P<movie_id>[0-9]+)/$', views.movie, name='movie'),
    url(r'^user(?P<user_id>[0-9]+)/$', views.user, name='user'),
    url(r'^redirect/', views.redirect, name='redirect'),
    url(r'rate_movie/(?P<movie_id>[0-9]+)/$', views.rate_movie, name='rate_movie')
]
