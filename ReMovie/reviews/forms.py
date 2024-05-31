from django import forms
from .models import Movie, Review
from django.core.validators import MinValueValidator, MaxValueValidator

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'director', 'release_date', 'cover_image'] 

    cover_image = forms.ImageField(required=False) 

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
