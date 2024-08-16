from datetime import timedelta

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from library.models import Book, BorrowedBook


class MyBooksView(generic.ListView):
    """
    Представление для отображения списка книг, взятых пользователем.
    """

    model = BorrowedBook
    template_name = "library/my_books.html"
    context_object_name = "borrowed_books"
    ordering = ["title"]

    def get_queryset(self):
        """
        Возвращает набор данных с книгами, заимствованными текущим пользователем.
        """
        return BorrowedBook.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs) -> dict:
        """
        Добавляет в контекст данные об уникальных заимствованных книгах.
        """
        context = super().get_context_data(**kwargs)
        borrowed_books = context["borrowed_books"]
        unique_books = {book.book.title: book for book in borrowed_books}.values()
        context["unique_books"] = unique_books
        return context


class DebtorListView(generic.ListView):
    """
    Представление отображающее список должников, которые не вернули книги
    в течение установленного времени (минутах).
    """

    model = BorrowedBook
    template_name = "library/debtor_list.html"
    context_object_name = "debtors"

    def get_queryset(self):
        """
        Возвращает список книг, которые были взяты, но не возвращены
        в течение указанного времени (в минутах).
        """
        overdue_minutes = 1  # Устанавливается количество минут, после которых пользователь считается должником
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        queryset = BorrowedBook.objects.filter(
            returned=False,
            borrowed_date__gte=today_start,
            borrowed_date__lte=timezone.now() - timedelta(minutes=overdue_minutes),
        )

        # Группируем по пользователю и книге, чтобы избежать дублирования
        unique_debtors = {}
        for book in queryset:
            key = (book.user_id, book.book_id)
            if key not in unique_debtors:
                unique_debtors[key] = book

        return list(unique_debtors.values())

    def get_context_data(self, **kwargs):
        """
        Добавляет информацию о времени (в минутах), в течение которого книга находится
        на руках у читателя, в контекст шаблона.
        """
        context = super().get_context_data(**kwargs)
        # Добавление количества минут, в течение которых книга на руках у читателя
        for debtor in context["debtors"]:
            debtor.minutes_borrowed = debtor.minutes_borrowed()
        return context


# Вставить блок для отображения списка должников, которые не вернули книги в течение установленного времени (днях)
#
# class DebtorListView(generic.ListView):
#     """
#     Представление отображающее список должников, которые не вернули книги
#     в течение установленного времени (днях).
#     """
#     model = BorrowedBook
#     template_name = 'library/debtor_list.html'
#     context_object_name = 'debtors'
#
# def get_queryset(self):
#     """
#     Возвращает список книг, которые были взяты, но не возвращены
#     в течение указанного времени (в минутах).
#     """
#     overdue_days = 14
#     # Фильтрация должников, которые не вернули книги более 14 дней
#     return BorrowedBook.objects.filter(returned=False,
#     borrowed_date__lte=timezone.now() - timedelta(days=overdue_days))
#
# def get_context_data(self, **kwargs):
#     """
#     Добавляет информацию о времени (в днях), в течение которого книга находится
#     на руках у читателя, в контекст шаблона.
#     """
#     context = super().get_context_data(**kwargs)
#     # Добавление количества дней, в течение которых книга на руках у читателя
#     for debtor in context['debtors']:
#         debtor.days_borrowed = debtor.days_borrowed()
#     return context


# Взять книгу
def borrow_book(request: HttpRequest, book_id: int) -> HttpResponse:
    """
    Функция для заимствования книги пользователем.
    """
    if request.user.is_authenticated:
        book = Book.objects.get(id=book_id)
        BorrowedBook.objects.create(book=book, user=request.user)
        return redirect("library:my_books")
    else:
        return redirect("users:login")


# Вернуть книгу
def return_book(request: HttpRequest, book_id: int) -> HttpResponse:
    """
    Функция для возврата книги пользователем.
    """
    if request.user.is_authenticated:
        BorrowedBook.objects.filter(book_id=book_id, user=request.user).delete()
        return redirect("library:my_books")
    else:
        return redirect("users:login")


# Список книг (Read)
class BookListView(generic.ListView):
    """
    Представление для отображения списка всех книг в библиотеке.
    """

    model = Book
    template_name = "library/book_list.html"
    context_object_name = "books"
    ordering = ["title"]


def get_context_data(self, **kwargs) -> dict:
    """
    Добавляет в контекст данные о заимствованных пользователем книгах.
    """
    context = super().get_context_data(**kwargs)
    context["borrowed_books"] = BorrowedBook.objects.filter(
        user=self.request.user
    ).values_list("book_id", flat=True)
    return context


# Детали книги (Read)
class BookDetailView(generic.DetailView):
    """
    Представление для отображения деталей конкретной книги.
    """

    model = Book
    template_name = "library/book_detail.html"
    context_object_name = "book"


# Создание книги (Create)
class BookCreateView(generic.CreateView):
    """
    Представление для создания новой книги в библиотеке.
    """

    model = Book
    template_name = "library/book_form.html"
    fields = ["title", "author", "genre"]
    success_url = reverse_lazy("library:book_list")


# Обновление книги (Update)
class BookUpdateView(generic.UpdateView):
    """
    Представление для обновления информации о книге.
    """

    model = Book
    template_name = "library/book_form.html"
    fields = ["title", "author", "genre"]
    success_url = reverse_lazy("library:book_list")


# Удаление книги (Delete)
class BookDeleteView(generic.DeleteView):
    """
    Представление для удаления книги из библиотеки.
    """

    model = Book
    template_name = "library/book_confirm_delete.html"
    success_url = reverse_lazy("library:book_list")
