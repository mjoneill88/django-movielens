from django import forms
from .models import Movie, Rater, Rating


class RaterForm(forms.ModelForm):
    age = forms.IntegerField(help_text="Please enter your age: ")
    sex = forms.ChoiceField(choices=Rater.sex_choices, help_text='Please enter your sex: ')
    occupation = forms.CharField(max_length=100, help_text='Please enter your occupation: ')
    zip_code = forms.CharField(max_length=5, help_text='Please enter your 5 digit zip/postal code: ')

    class Meta:
        model = Rater
        fields = ('age', 'sex', 'occupation', 'zip_code')


class RatingForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=Rating.rating_choices, help_text='Please enter your rating: ')

    class Meta:
        model = Rating
        fields = ('rating', )
