from django.urls import path

from .views import (
    UserRetrieveAPIView,
    LoginView,
    LogoutView,
    UserSignUpView,
    VerifyEmailView,
    PasswordResetEmailView,
    PasswordResetView,
)

urlpatterns = [
    path("<uuid:pk>/", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("activate/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path(
        "send-password-reset-email/",
        PasswordResetEmailView.as_view(),
        name="send-password-reset-email",
    ),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
]
