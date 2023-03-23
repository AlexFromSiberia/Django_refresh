from django.db import models


class Categories(models.Model):
    """Категории фильмов"""
    name = models.CharField('Категория', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    """Актёры и режиссеры"""
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актёры и режиссеры'
        verbose_name_plural = 'Актёры и режиссеры'



