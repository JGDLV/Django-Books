from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Author(models.Model):
    ''' Модель автора '''

    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    slug = models.SlugField('Слаг', unique=True, max_length=200)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name']

    def get_absolute_url(self):
        return reverse('authors_detail', kwargs={'slug': self.slug})

    def first_letter(self):
        return self.last_name and self.last_name[0] or ''

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Genre(models.Model):
    ''' Модель жанра '''

    title = models.CharField('Название', max_length=100)
    slug = models.SlugField('Слаг', unique=True, max_length=100)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('genres_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Book(models.Model):
    ''' Модель книги '''

    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка', blank=True,
                              null=True, upload_to='books/')
    description = models.TextField('Описание')
    authors = models.ManyToManyField(
        Author, related_name='authors', blank=True, null=True, verbose_name='Авторы')
    genres = models.ManyToManyField(
        Genre, related_name='genres', verbose_name='Жанры')
    isbn = models.CharField('ISBN', max_length=13)
    year = models.CharField('Год', max_length=4, blank=True, null=True)
    slug = models.SlugField('Слаг', unique=True, max_length=200)
    users = models.ManyToManyField(
        User, related_name='bookmarks', blank=True, null=True, verbose_name='Закладки')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('books_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Пользователь')
    book = models.ForeignKey(Book, null=True, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Книга')
    text = models.TextField('Комментарий', max_length=700)
    date = models.DateTimeField('Дата и время', auto_now_add=True)
    moderation = models.BooleanField('На модерации', default=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date']

    def __str__(self):
        return self.text
