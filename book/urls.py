

from django.urls import path

from . import views

urlpatterns = [
    path('search-books/', views.search_books, name='search_books'),
    path('mark-as-read/', views.mark_as_read, name='mark_as_read'),
    path('book_list/', views.book_list, name='book_list'),
]
