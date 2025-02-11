from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    avatar = models.ImageField(
        upload_to="avatars/", default="avatars/default_avatar.jpg", blank=True, null=True, verbose_name="Аватар"
    )
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна")

    token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Токен")
    password_reset_token = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Токен для сброса пароля"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = [
            "email",
        ]
        permissions = [("can_block_user", "Может блокировать пользователя")]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
