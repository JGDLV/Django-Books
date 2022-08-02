from django.contrib import admin
from django.utils.safestring import mark_safe
from . import models


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_authors',
                    'get_genres', 'isbn', 'year',)
    list_display_links = ('title',)
    # list_editable = ('year', 'isbn',)
    prepopulated_fields = {'slug': ('title',), }
    save_as = True
    save_on_top = True
    ordering = ('id',)
    readonly_fields = ('get_image',)
    fields = ('title', 'slug', 'image', 'get_image', 'description',
              'authors', 'genres', 'isbn', 'year', 'users',)
    # fieldsets = (
    #     ('', {'fields': (('title', 'slug',),)}),
    #     ('', {'fields': (('image',),)}),
    #     ('', {'fields': (('get_image',),)}),
    #     ('', {'fields': (('description',),)}),
    #     ('', {'fields': (('authors', 'genres',),)}),
    #     ('', {'fields': (('isbn',),)}),
    #     ('', {'fields': (('year',),)}),
    #     ('', {'fields': (('users',),)}),
    # )

    def get_image(self, obj):
        return mark_safe(f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}" width="200" style="border: 1px solid #ddd;"></a>')

    def get_image_small(self, obj):
        return mark_safe(f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}" width="50" style="border: 1px solid #ddd;"></a>')

    def get_genres(self, obj):
        return ', '.join([str(i.title) for i in obj.genres.all()])

    def get_authors(self, obj):
        return ', '.join([str(f'{i.first_name} {i.last_name}') for i in obj.authors.all()]) or '-'

    get_image.short_description = 'Превью'
    get_image_small.short_description = 'Превью'
    get_genres.short_description = 'Жанры'
    get_authors.short_description = 'Авторы'


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'get_books',)
    list_display_links = ('get_full_name', )
    prepopulated_fields = {'slug': ('first_name', 'last_name'), }
    save_as = True
    save_on_top = True
    ordering = ('last_name',)

    def get_full_name(self, obj):
        return f'{obj.last_name}, {obj.first_name}'

    def get_books(self, obj):
        return obj.authors.all().count()

    get_books.short_description = 'Количество книг'
    get_full_name.short_description = 'Полное имя'


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_books',)
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',), }
    save_as = True
    save_on_top = True
    ordering = ('title',)

    def get_books(self, obj):
        return obj.genres.all().count()

    get_books.short_description = 'Количество книг'


@admin.register(models.Comment)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('date', 'moderation', 'book', 'user', 'get_text', )
    list_display_links = ('get_text',)
    list_editable = ('moderation',)
    save_as = True
    save_on_top = True
    # ordering = ('id',)

    def get_text(self, obj):
        if len(obj.text) >= 100:
            return obj.text[0:100] + ' ...'
        else:
            return obj.text[0:100]

    get_text.short_description = 'Комментарий'
