from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin

from users.forms import UserProfileForm, UserLoginForm, ReaderRegisterForm, LibrarianRegisterForm
from users.models import User


# Регистрация читателя
class ReaderRegisterView(CreateView):
    """
    Представление для регистрации читателя.
    """
    form_class = ReaderRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


# Регистрация библиотекаря
class LibrarianRegisterView(CreateView):
    """
    Представление для регистрации библиотекаря.
    """
    form_class = LibrarianRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


# Вход пользователя
class UserLoginView(BaseLoginView):
    """
    Представление для авторизации пользователя на сайте.
    """
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст.
        """
        context = super().get_context_data(**kwargs)
        return context


# Выход пользователя
class UserLogoutView(BaseLogoutView):
    """
    Представление для выхода пользователя из системы.
    """
    success_url = reverse_lazy('library:book_list')

# Профиль пользователя
class ProfileView(UpdateView):
    """
    Представление для просмотра и редактирования профиля пользователя.
    """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None) -> User:
        """
        Возвращает текущего авторизованного пользователя.
        """
        return self.request.user
