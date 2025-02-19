from django.urls import path

from .apps import UsersConfig
from .views import (
    ChangeUserStatusView,
    CustomLoginView,
    CustomLogoutView,
    EditProfileUpdateView,
    PasswordResetRequestView,
    RegisterView,
    UserProfileDetailView,
    UsersListView,
    email_verification,
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm"),
    path("profile/edit/<int:pk>/", EditProfileUpdateView.as_view(), name="edit_profile"),
    path("all-users/", UsersListView.as_view(), name="all_users"),
    path("profile/<int:pk>/", UserProfileDetailView.as_view(), name="user_profile"),
    path("change-status/<int:pk>/", ChangeUserStatusView.as_view(), name="change_user_status"),
    path("password-reset-request/", PasswordResetRequestView.as_view(), name="password_reset_request"),
]
