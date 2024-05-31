from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.db.models import Avg
from .models import Movie, Stats, Review
from .forms import ReviewForm, MovieForm
from django.http import HttpResponseBadRequest

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    # Pobierz recenzję użytkownika dla danego filmu
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(user=request.user, movie=movie).first()
    
    return render(request, 'movie_detail.html', {'movie': movie, 'user_review': user_review})

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_detail', movie_id=movie.id)
    else:
        review_form = ReviewForm()
    return render(request, 'add_review.html', {'review_form': review_form, 'movie': movie})

@login_required
def user_stats(request):
    user = request.user
    stats, created = Stats.objects.get_or_create(user=user)
    
    # Obliczanie średniej oceny filmów
    reviews = Review.objects.filter(user=user)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0
    
    stats.average_rating = average_rating
    stats.movies_watched = reviews.count()
    stats.save()
    
    movies = Movie.objects.filter(review__user=user).distinct()  # Dodaj tę linię, aby uzyskać listę obejrzanych filmów przez użytkownika
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'user_stats.html', {'stats': stats, 'user': user, 'movies': movies, 'reviews': reviews})

@login_required
def add_movie_and_review(request):
    if request.method == 'POST':
        movie_form = MovieForm(request.POST, request.FILES)  # Dodaj request.FILES
        review_form = ReviewForm(request.POST)
        if movie_form.is_valid() and review_form.is_valid():
            movie = movie_form.save(commit=False)
            if 'cover_image' in request.FILES:
                print("Obraz jest przesyłany")  # Dodaj debugowanie
                movie.cover_image = request.FILES['cover_image']
            movie.save()
            review = review_form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()

            # Update user stats
            user = request.user
            user.stats.movies_watched = Movie.objects.filter(review__user=user).count()
            user.stats.average_rating = Review.objects.filter(user=user).aggregate(Avg('rating'))['rating__avg']
            user.stats.save()

            return redirect('user_stats')
        else:
            print("Błąd w formularzu")
            print(movie_form.errors, review_form.errors)
    else:
        movie_form = MovieForm()
        review_form = ReviewForm()
    return render(request, 'add_movie_and_review.html', {'movie_form': movie_form, 'review_form': review_form})

@login_required
def delete_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_id)
        if review.user == request.user:
            review.delete()
            return redirect('movie_detail', movie_id=review.movie.id)
        else:
            return HttpResponseBadRequest("You are not allowed to delete this review.")
    else:
        return HttpResponseBadRequest("Invalid request method.")

@login_required
def delete_movie_with_reviews(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    # Usuwamy film wraz z recenzjami
    movie.delete()
    return redirect('movie_list')
