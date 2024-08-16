from django.urls import path

from users.views import (
    LibrarianRegisterView,
    ProfileView,
    ReaderRegisterView,
    UserLoginView,
    UserLogoutView,
)

app_name = "users"


urlpatterns = [
    path("register/reader/", ReaderRegisterView.as_view(), name="register_reader"),
    path(
        "register/librarian/",
        LibrarianRegisterView.as_view(),
        name="register_librarian",
    ),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
