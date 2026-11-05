from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    """
    Роли пользователей.
    """
    USER = 'user', 'Пользователь'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):
    """
    Модель Пользователь.
    Базовые поля (username, пароль, email, сессии, права)
    наследуются от AbstractUser.
    """

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self) -> str:
        return f'Пользователь: {self.username} ({self.get_role_display()})'
