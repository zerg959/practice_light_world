from django.db import models
from django.conf import settings
import uuid


class StationStatus(models.TextChoices):
    """
    Возможные статусы станции.
    """
    ONLINE = ('online', 'Онлайн')
    OFFLINE = ('offline', 'Офлайн')


class ConfigStatus(models.TextChoices): 
    """
    Возможные статусы Конфигурации.
    """
    PUBLISHED = ('published', 'Опубликовано') 
    APPLIED = ('applied', 'Применено')
    DEPRECATED = ('deprecated', 'Устарело')


class ControllerStatus(models.TextChoices):
    """
    Возмодные статусы Контроллера.
    """
    ONLINE = ('online', 'Онлайн')
    OFFLINE = ('offline', 'Офлайн')
    ERROR = ('error', 'Ошибка')


class Station(models.Model):
    """
    Модель Станция.
    Содержит слоты для хранения объектов выдачи.
    Содержит примененную Конфигурацию Станиции
    """

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
        choices=StationStatus.choices,
        default=StationStatus.OFFLINE,
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

    station = models.ForeignKey(
        'stations.Station',
        on_delete=models.CASCADE,
        related_name="configs",
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
        choices=ConfigStatus.choices,
        default=ConfigStatus.PUBLISHED,
        max_length=20,
        verbose_name="Статус конфигурации",
        help_text="Текущий статус конфигурации: Опубликовано/Применено/Устарело"
    )

    snapshot = models.JSONField(
        blank=True,
        default=dict,
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
        related_name="created_configs",
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
                name="uniq_vers_per_stat"),
            models.UniqueConstraint(
                fields=['station'], condition=models.Q(status=ConfigStatus.APPLIED),
                name="uniq_applied_vers_per_stat")
                ]

    def __str__(self) -> str:
        return f'Версия: {self.version_number}, от {self.created_at}, {self.status}'


class Controller(models.Model):
    """
    Модель Контроллер.
    Осуществляет управление ячейкой через каналы (1-16).
    Один контроллер на станцию, один канал на ячейку.
    Связи Контроллер - Станция и Канал - Ячейка уникальны.

    Статусы и время последнего отклика обновляет воркер,
    обрабатывающий SensorEvent (heartbeat / PING-ответы).
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="UUID",
        help_text="Уникальный ID контроллера",
    )

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
    status = models.CharField(
        max_length=10,
        choices=ControllerStatus.choices,
        default=ControllerStatus.OFFLINE,
        verbose_name="Статус контроллера",
        help_text="Актуальный статус связи: онлайн/офлайн/ошибка",
    )
    last_seen_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Последний отклик",
        help_text="Время последнего события или PING-ответа от контроллера",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата создания записи",
    )

    class Meta:
        verbose_name = "Контроллер"
        verbose_name_plural = "Контроллеры"
        ordering = ('station', 'serial_number')
        indexes = [
            models.Index(fields=['status'], name='ctrl_status_idx'),
            models.Index(fields=['station', 'status'],
                         name='ctrl_station_status_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['station'],
                name='uniq_controller_per_station',
            ),
        ]

    def __str__(self) -> str:
        return f"Контроллер {self.serial_number} -> ст.  {self.station_id}, {self.get_status_display()}"
