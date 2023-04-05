from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView
from .models import Movie, Category, Actor, Genre
from .forms import ReviewForm


class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        """Возвращает список жанров"""
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year').distinct()


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movie_list.html'


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    template_name = 'movies/movie_detail.html'
    slug_field = 'url'


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie_id = pk
            form.save()
        return redirect(Movie.objects.get(id=pk).get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод инфо об актёре"""
    model = Actor
    template_name ='movies/actor.html'
    # Бывает, что вам нужно добавить отображение к существующей модели. Если в этой модели есть поле SlugField,
    # но оно не называется slug, и вы хотите создать адрес по этому полю,
    # Просто переопределите атрибут slug_field.
    slug_field = 'name'