from django import forms
from .models import Movie, Review
from django.core.validators import MinValueValidator, MaxValueValidator

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'director', 'release_date', 'cover_image']  # Dodaj pole cover_image

    cover_image = forms.ImageField(required=False)  # Dodaj to pole, aby obsłużyć pliki obrazów

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
