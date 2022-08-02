"""books_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from books import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('books/', views.BooksList.as_view(), name='books_list'),
    path('books/<slug:slug>', views.BooksDetail.as_view(), name='books_detail'),
    path('authors/', views.AuthorsList.as_view(), name='authors_list'),
    path('authors/<slug:slug>', views.AuthorsDetail.as_view(), name='authors_detail'),
    path('genres/', views.GenresList.as_view(), name='genres_list'),
    path('genres/<slug:slug>', views.GenresDetail.as_view(), name='genres_detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/profile/bookmarks/', views.ProfileBookmarksView.as_view(), name='profile_bookmarks'),
    path('accounts/profile/comments/', views.ProfileCommentsView.as_view(), name='profile_comments'),
    path('bookmarks/change/<int:id>/', views.BookmarksAdd.as_view(), name='bookmarks_add'),
    # path('bookmarks/remove/<int:id>/', views.BookmarksRemove.as_view(), name='bookmarks_remove'),
    path('comment/<int:id>/', views.CommentAdd.as_view(), name='comment_add'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
