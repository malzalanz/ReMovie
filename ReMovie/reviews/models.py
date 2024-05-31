from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    director = models.CharField(max_length=255)
    release_date = models.CharField(max_length=4)  # Zmiana pola na pole CharField dla roku
    cover_image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} for {self.movie.title}"

class Stats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movies_watched = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0)
