# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-06 19:54
from __future__ import unicode_literals

from django.db import migrations, models
from movie_recommender.models import Rater
from django.contrib.auth.models import User


def populate_user_in_rating(apps, schema_editor):
    for one_user in User.objects.all():
        if one_user.username[:-1] == 'rater':
            one_rater = Rater.objects.get(rater_id=one_user.username[-1])
            one_rater.user = one_user
            one_rater.save()


class Migration(migrations.Migration):

    dependencies = [
        ('movie_recommender', '0003_auto_20160506_1954'),
    ]

    operations = [
    migrations.RunPython(populate_user_in_rating),
    ]
