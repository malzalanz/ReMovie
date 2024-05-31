# urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import movie_list, movie_detail, add_review, user_stats, RegisterView, add_movie_and_review
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('add_movie_and_review/', add_movie_and_review, name='add_movie_and_review'),
    path('', user_stats, name='user_stats'),  # Domyślny widok, przekierowanie do user_stats
    path('movies/', movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/add_review/', add_review, name='add_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('delete_movie_with_reviews/<int:movie_id>/', views.delete_movie_with_reviews, name='delete_movie_with_reviews'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
]

# Dodajmy obsługę dla plików multimedialnych (np. obrazy)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
