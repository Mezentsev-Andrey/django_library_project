from django.forms import forms
from django.forms.fields import BooleanField
from library.models import Book


class StyleFormMixin:
    """
    Миксин для добавления CSS классов к полям формы в зависимости от их типа.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class BookForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания и обновления книги.
    """

    class Meta:
        model = Book
        fields = ('title', 'author', 'genre', 'description')
