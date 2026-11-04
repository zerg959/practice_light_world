from typing import Any
from django.db import models
from django.conf import settings


class Station(models.Model):
    """
    Модель Станция.
    Содержит слоты для хранения объектов выдачи.
    Содержит примененную Конфигурацию Станиции
    """

    class Status(models.TextChoices):
        """
        Возможные статусы станции.
        """
        ONLINE = ('online', 'Онлайн')
        OFFLINE = ('offline', 'Офлайн')

    location = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Расположение",
        help_text="Координаты станции"
    )
    current_applied_config_version = models.ForeignKey(
       'stations.StationConfig',
       on_delete=models.PROTECT,  # конфиг не удалить. если он используется
       null=True,
       related_name="stations_with_curr_conf",
       verbose_name="Текущая примененная версия конфигурации",
       help_text="Активная версия конфигурации"
       )
    station_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OFFLINE,
        verbose_name='Статус станции',
        help_text="например: Онлайн/Офлайн"
    )

    class Meta:
        verbose_name = "Станция"
        verbose_name_plural = "Станции"
        ordering = ['-id',]

    def __str__(self) -> str:
        return f"Станция {self.id} - {self.get_station_status_display()}"


class StationConfig(models.Model):
    '''
    Модель для хранения опубликованных(published), но не примененных 
    конфигураций станций.
    Используемые (applied) версии записываются в БД и применяются в поле
    current_applied_config.
    '''
    class Status(models.TextChoices): 
        """
        Возможные статусы Конфигурации.
        """
        PUBLISHED = ('published', 'Опубликовано') 
        APPLIED = ('applied', 'Применено')
        DEPRECATED = ('deprecated', 'Устарело')
    station = models.ForeignKey(
        'stations.Station',
        on_delete=models.CASCADE,
        related_name="configs",
        null=True,
        blank=True,
        verbose_name="Станция",
        help_text="Станция, где применена конфигурация"
    )

    version_number = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        verbose_name="Версия",
        help_text="Номер версии (напимер: 1.1)"
    )
    status = models.CharField(
        choises=Status.choices,
        default=Status.PUBLISHED,
        max_length=20,
        verbose_name="Статус конфигурации",
        help_text="Текущий статус конфигурации: Опубликовано/Применено/Устарело"
    )
    snapshot = models.JSONField(
        blank=True,
        verbose_name="Снапшот примененной конфигурации",
        help_text="JSON-копия конфигурации на момент публикации"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания конфигурации"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="users",
        verbose_name="Автор",
        help_text="Пользователь, создавший конфигурацию"
        )

    class Meta:
        verbose_name = 'Конфигурация'
        verbose_name_plural = 'Конфигурации'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['station', 'status'],
                         name="st_conf_status_idx"),
            models.Index(fields=['status'],
                         name="conf_stat_idx")
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['station', 'version_number'],
                name="unique_version_per_station"),
            models.UniqueConstraint(
                fields=['station'], condition=models.Q(status=Status.APPLIED),
                name="unique_applied_version_per_station")
                ]

    def __str__(self) -> str:
        return f'Версия: {self.version_number}, от {self.created_at}, {self.status}'


class Controller(models.Model):
    """
    Модель Контроллер.
    Осуществляет управление ячейкой через каналы (1-16).
    Один контроллер на станцию, один канал на ячейку.
    Связи Контроллер - Станция и Канал - Ячейка уникальны.
    """
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Название контроллера",
        help_text="Человекочитаемое название контроллера"
        )
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Серийный номер",
        help_text="Уникальный серийный номер контроллера"
        )
    station = models.ForeignKey(
        'stations.Station',
        on_delete=models.PROTECT,
        related_name="controllers",
        verbose_name="Станция",
        help_text="Станция, к которой подключен контроллер"
        )

    class Meta:
        verbose_name = "Контроллер"
        verbose_name_plural = "Контроллеры"

        def __str__(self) -> str:
            return f"Контроллер {self.serial_number} -> ст. {self.station}"
