from django.db import models


class User(models.Model):
    """
    Модель Пользователь
    """
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Имя пользователя',
        help_text='Уникальное имя пользователя'
        )

    role = models.TextChoices(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )

    class Meta:
        vebose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self) -> str:
        return f'Пользователь: {self.username} - ({self.get_role_display()})'
