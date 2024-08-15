
from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Book(models.Model):
    """
    Модель, представляющая книгу в библиотеке.
    """
    title = models.CharField(max_length=100, verbose_name='Название книги')
    author = models.CharField(max_length=100, verbose_name='Автор')
    genre = models.CharField(max_length=50, verbose_name='Жанр', **NULLABLE)
    cover = models.ImageField(upload_to='books/', verbose_name='Обложка', **NULLABLE)
    description = models.TextField(verbose_name='Аннотация', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class BorrowedBook(models.Model):
    """
    Модель, представляющая взятую книгу пользователем.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Взятая книга')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Читатель')
    borrowed_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения книги')
    returned_date = models.DateTimeField(verbose_name='Дата возврата книги', **NULLABLE)
    returned = models.BooleanField(default=False)

    def minutes_borrowed(self):
        """
        Рассчитывает количество минут, в течение которых книга была взята.
        """
        end_time = self.returned_date if self.returned else timezone.now()
        # Проверка, если книга была взята и возвращена в один и тот же день
        if self.borrowed_date.date() == end_time.date():
            return int((end_time - self.borrowed_date).total_seconds() // 60)
        else:
            # Если книга была взята в один день и возвращена в другой, считаем только минуты в день взятия и день возврата
            start_of_end_day = end_time.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_borrowed_day = self.borrowed_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            return int((end_of_borrowed_day - self.borrowed_date).total_seconds() // 60) + int(
                (end_time - start_of_end_day).total_seconds() // 60)

    def __str__(self):
        return f'{self.user.username} взял {self.book.title}'

    class Meta:
        verbose_name = 'Взятая книга'
        verbose_name_plural = 'Взятые книги'

    # Вставить блок для расчета дней в течение установленного времени (днях)
    #
    # def days_borrowed(self):
    # """
    # Рассчитывает количество дней, в течение которых книга была взята.
    # """
    #     end_date = self.returned_date if self.returned else timezone.now().date()
    #     return (end_date - self.borrowed_date.date()).days
