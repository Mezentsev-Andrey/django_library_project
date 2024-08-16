from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Модель пользователя.
    """

    LIBRARIAN = "librarian"
    READER = "reader"

    ROLE_CHOICES = [
        (LIBRARIAN, "Библиотекарь"),
        (READER, "Читатель"),
    ]

    username = models.CharField(max_length=30, unique=True, verbose_name="Логин")
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, verbose_name="Тип пользователя"
    )
    employee_number = models.CharField(
        max_length=20, verbose_name="Табельный номер", **NULLABLE
    )
    first_name = models.CharField(max_length=30, verbose_name="Имя", **NULLABLE)
    last_name = models.CharField(max_length=30, verbose_name="Фамилия", **NULLABLE)
    address = models.TextField(verbose_name="Адрес", **NULLABLE)
    is_reader = models.BooleanField(default=False, verbose_name="Читатель")
    is_librarian = models.BooleanField(default=False, verbose_name="Библиотекарь")

    def __str__(self) -> str:
        return f"{self.username}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
