from re import template
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.db.models import Q
from . import models, forms


class HomeView(View):
    ''' Домашняя страница '''

    def get(self, request):
        books = models.Book.objects.all()[:10]
        return render(request, 'books/home.html', {
            'title': '100 лучших книг',
            'books': books,
        })


class BooksList(ListView):
    ''' Список книг '''

    model = models.Book
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # all_years = models.Book.objects.all().values_list('year', flat=True)
        # context['min_year'] = min(all_years)
        # context['max_year'] = max(all_years)
        context['title'] = 'Книги'
        return context


class BooksDetail(DetailView):
    ''' Книга '''

    model = models.Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = models.Comment.objects.filter(
            book=self.object.id, moderation=False)
        context['form'] = forms.CommentForm()
        return context


class AuthorsList(ListView):
    ''' Список авторов '''

    model = models.Author
    # context_object_name = 'authors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторы'
        return context


class AuthorsDetail(DetailView):
    ''' Автор '''

    model = models.Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = models.Book.objects.filter(authors=self.object.id)
        return context


class GenresList(ListView):
    ''' Список жанров '''

    model = models.Genre
    # context_object_name = 'genres'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Жанры'
        return context


class GenresDetail(DetailView, MultipleObjectMixin):
    ''' Жанр '''

    model = models.Genre
    paginate_by = 10

    def get_context_data(self, **kwargs):
        books = models.Book.objects.filter(genres=self.object.id)
        context = super(GenresDetail, self).get_context_data(
            object_list=books, **kwargs)
        return context


class SearchView(View):
    ''' Результаты поиска '''

    def get(self, request):
        q = request.GET.get('q')
        books = models.Book.objects.filter(
            Q(title__icontains=q) | Q(isbn__icontains=q)).order_by('title')
        authors = models.Author.objects.filter(last_name__icontains=q)
        genres = models.Genre.objects.filter(title__icontains=q)
        return render(request, 'books/search.html', {
            'title': 'Результаты поиска',
            'books': books,
            'authors': authors,
            'genres': genres,
        })


class ProfileView(View):
    ''' Профиль пользователя '''

    def get(self, request):
        if request.user.is_authenticated:
            bookmarks_counter = len(
                models.Book.objects.filter(users=request.user))
            comments_counter = len(
                models.Comment.objects.filter(user=request.user))
            return render(request, 'books/profile.html', {
                'title': 'Профиль пользователя',
                'bookmarks_counter': bookmarks_counter,
                'comments_counter': comments_counter,
            })
        else:
            return redirect('account_login')


class BookmarksAdd(View):
    ''' Добавление и удаление из закладок в списке '''

    def post(self, request, id):
        book = models.Book.objects.get(pk=id)
        if request.POST.get('bookmark') == 'on':
            book.users.remove(request.user)
            book.save()
            return redirect('home')
        else:
            book.users.add(request.user)
            book.save()
            return redirect('home')


# class BookmarksRemove(View):
#     ''' Удаление из закладок в детальном просмотре '''

#     def post(self, request, id):
#         book = models.Book.objects.get(pk=id)
#         book.users.remove(request.user)
#         book.save()
#         return redirect('profile')


class CommentAdd(View):
    ''' Добавление комментария '''

    def post(self, request, id):
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = request.user.id
            form.book_id = id
            form.save()
        return redirect('home')


class ProfileBookmarksView(ListView):
    ''' Закладки в профиле пользователя '''

    model = models.Book
    paginate_by = 10
    template_name = 'books/bookmark_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(users=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои закладки'
        return context


class ProfileCommentsView(ListView):
    ''' Комментарии в профиле пользователя '''

    model = models.Comment
    paginate_by = 10
    template_name = 'books/comment_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои комментарии'
        return context
