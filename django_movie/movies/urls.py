from django.urls import path
from .views import MoviesView


urlpatterns = [
    path('', MoviesView.as_view(), name='movie_list'),
]