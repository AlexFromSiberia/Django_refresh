from django import template
from movies.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies():
    """Вывод последних фильмов"""
    movies = Movie.objects.order_by('-id')[:5]
    return {'movies': movies}
