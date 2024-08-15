from django import forms
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    """
    Форма авторизации на сайте.
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class ReaderRegisterForm(UserCreationForm):
    """
    Форма регистрации читателя библиотеки.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'address', 'password1', 'password2', 'is_reader']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.READER
        if commit:
            user.save()
        return user


class LibrarianRegisterForm(UserCreationForm):
    """
    Форма регистрации библиотекаря.
    """
    class Meta:
        model = User
        fields = ['username', 'employee_number', 'password1', 'password2', 'is_librarian']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.LIBRARIAN
        if commit:
            user.save()
        return user


class UserProfileForm(UserChangeForm):
    """
    Форма профиля пользователя.
    """
    class Meta:
        model = User
        fields = ('username', 'role', 'employee_number', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

        self.fields['password'].widget = forms.HiddenInput()
