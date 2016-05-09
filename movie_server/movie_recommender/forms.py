from django.forms import ModelForm
from .models import Movie, Rater, Rating


class RaterForm(ModelForm):
    class Meta:
        model = Rater
        fields = ('rater_id', 'age', 'sex', 'occupation', 'zip_code')


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ('rating', )
