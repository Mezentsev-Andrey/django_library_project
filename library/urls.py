from django.urls import path

from library.views import (BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView,
                           MyBooksView, borrow_book, return_book, DebtorListView)

app_name = 'library'

urlpatterns = [
    path('my_books/', MyBooksView.as_view(), name='my_books'),
    path('debtors/', DebtorListView.as_view(), name='debtor_books'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('return/<int:book_id>/', return_book, name='return_book'),

    path('', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('books/edit/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
]
