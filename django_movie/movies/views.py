from django.views.generic import DetailView, ListView
from .models import Movie


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'


class MovieDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    template_name = 'movies/movie_detail.html'
    slug_field = 'url'

