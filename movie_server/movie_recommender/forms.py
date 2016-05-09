from django import forms
from django.template import RequestContext
from .models import Movie, Rater, Rating


class RaterForm(forms.ModelForm):
    class Meta:
        model = Rater
        fields = ('rater_id', 'age', 'sex', 'occupation', 'zip_code')


class RatingForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=Rating.rating_choices, help_text='Please enter your rating:')
    class Meta:
        model = Rating
        fields = ('rating', )
