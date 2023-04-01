from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, Reviews, RatingStar
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    """Форма для CKEditor"""
	# content - field in our model
    description = forms.CharField(label="Описание",  widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


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
    classes = ['collapse']


class MovieShotsInline(admin.TabularInline):
    """Для отображения кадров из фильма в модели Фильмы"""
    model = MovieShots
    extra = 1
    classes = ['collapse']

    readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="100">')
        return '-'

    get_image.short_description = 'Кадры из фильма'


class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    # form - форма для ckeditor
    form = MovieAdminForm
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
            'fields': (('description', 'poster', 'get_image'),)
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

    readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.poster:
            return mark_safe(f'<img src={obj.poster.url} width="100">')
        return '-'

    get_image.short_description = 'Постер'
    # регестрируем экшены
    actions = ['unpublish', 'publish']

    def unpublish(self, request, queryset):
        """Unpublish the movie"""
        # выполняемое действие - статус черновика в Тру
        row_update = queryset.update(draft=True)
        # тут описываем сообщение по завершению.
        # Зависит один или несколько обьектов были выбраны
        if row_update == 1:
            message_bit = '1 Запись успешно обновлена'
        else:
            message_bit = f'{row_update} Записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """publish the movie"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 Запись успешно обновлена'
        else:
            message_bit = f'{row_update} Записей были обновлены'
        self.message_user(request, f'{message_bit}')

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    publish.short_description = 'Публиковать'
    publish.allowed_permissions = ('change',)


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

    get_image.short_description = 'Фото актера'


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