from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, Reviews, RatingStar


class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links = ("name", )


# доп класс - позволит выводить все комментарии к фильму
# отношение ForeignKey
class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Reviews
    # определяет сколько "пустых" заготовок будет в выведенном списке
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInline(admin.TabularInline):
    """Для отображения кадров из фильма в модели Фильмы"""
    model = MovieShots
    extra = 1

    readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="50" >')
        return '-'

    get_image.short_description = 'Изображение'


class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline, ]  # нужен доп класс 'NameInline'
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    # выводит поля указанными сетами в одну линию
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),

        (None, {
            'fields': (('description', 'poster'),)
        }),

        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),

        ('Actors', {
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),

        ('Options', {
            'fields': (('url', 'draft'),)
        }),
    )


class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ('name', 'url')


class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="50" >')
        return '-'

    get_image.short_description = 'Изображение'


class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip", "star")


class MovieShotsAdmin(admin.ModelAdmin):
    """Фотографии"""
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="50" >')
        return '-'

    get_image.short_description = 'Изображение'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieShots, MovieShotsAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Reviews, ReviewAdmin)
admin.site.register(RatingStar)

admin.site.site_header = 'Проект Фильмы'