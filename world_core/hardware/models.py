from django.db import models
from django.core.validators import (MinValueValidator, MaxValueValidator)
from django.db.models import Q
import uuid


class HardwareCommand(models.Model):
    """
    Модель описывает очередь исходящих команд.
    Слой коммуникации для реализации физических действий через Контроллер.
    Позволяет ставить команды в очередь, отслеживать статусы
    (pending → sent → acked/failed/timeout) и отменять ещё не отправленные.
    Например: Открыть или закрыть ячейку.
    """

    class CommandType(models.TextChoices):
        """
        Типы команды.
        """
        OPEN_LOCK = ("open_lock", "Открыть замок")
        GET_STATUS = ("get_status", "Получить статус")
        REBOOT = ("reboot", "Перезагрузить")
        PING = ("ping", "Установить связь")

    class Status(models.TextChoices):
        """
        Статусы команды.
        """
        PENDING = ("pending", "Ожидание")
        SENT = ("sent", "Отправлено")
        ACKED = ("acked", "Подтверждено")
        FAILED = ("failed", "Неудачно")
        TIMEOUT = ("timeout", "Таймаут")
        CANCELLED = ("cancelled", "Отменено")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Уникальный идентификатор команды (UUID4)"
    )

    controller = models.ForeignKey(
        "stations.Controller",
        on_delete=models.CASCADE,
        related_name="commands",
        help_text="Контроллер",
        )

    channel = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Номер канала не может быть меньше 1'),
            MaxValueValidator(16, message='Номер канала не может быть больше 16')
            ],
        help_text="Номер канала (1-16)."
        "На один канал одного контроллера может быть только одна "
        "активная команда (со статусом pending или sent). Повторная "
        "активная команда вызовет ошибку 400/409. Реализовано через "
        "constraints в Meta"
        )
    command_type = models.CharField(
        max_length=15,
        choices=CommandType.choices,
        default=CommandType.GET_STATUS,
        help_text=(
            "Тип команды. "
            "Комбинация (controller, channel, command_type) "
            "должна быть уникальной "
            "среди активных команд (pending/sent)."
        )
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
        help_text="Текущий статус команды"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Время создания"
        )
    # sent_at = models.DateTimeField()
    # finished_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['controller', 'status'],
                         name='hw_cntrl_status_index'),
            models.Index(fields=['status'], name='hw_status_index')
            ]
        ordering = ('-created_at',)
        verbose_name = "Очередь исходящих команд"
        verbose_name_plural = "Очереди исходящих команд"
        constraints = [
            models.UniqueConstraint(
                fields=['controller', 'channel', 'command_type'],
                condition=Q(status__in=[Status.SENT, Status.PENDING]),
                name='unique_active_command_per_channel')
            ]

    def __str__(self):
        return f"Команда {self.command_type} на канал {self.channel} ({self.status})"


class SensorEvent(models.Model):
    """
    Журнал входящих событий (raw data) от Контроллера.

    Примечание: В воркере, который разбирает события:
    Перед попыткой: attempts += 1.
    Удалось: processing_status = DONE, processed_at=timezone.now(), processing_error = None.
    Не удалось: processing_status = FAILED, в processing_error пишем текст ошибки.
    ретрай-воркер берёт всё с processing_status=FAILED (и, если нужно, attempts < N
    (для ограничения попыток)).
    """
    class EventType(models.TextChoices):
        """
        Типы событий от Контроллера.
        """
        DOOR_OPEN = ('door_open', 'Дверь открыта')
        DOOR_CLOSE = ('door_close', 'Дверь закрыта')
        REBOOT = ('reboot', 'Перезагрузка')
        ERROR = ('error', 'Ошибка')

    class ProcessStatus(models.TextChoices):
        PENDING = ('pending', 'Ожидает обработки')
        DONE = ('done', 'Обработано')
        FAILED = ('failed', 'Ошибка обработки')

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Уникальный идентификатор события (UUID4)"
    )
    controller = models.ForeignKey(
        'stations.Controller',
        on_delete=models.PROTECT,
        related_name="events",
        help_text="Контроллер"
        )
    channel = models.IntegerField(
        validators=[
            MinValueValidator(1, message="номер канала не может быть меньше 1"),
            MaxValueValidator(16, message="номер канала не может быть больше 16"),
            ],
        null=True,
        blank=True,
        help_text="Номер канала"
        )
    event_type = models.CharField(
        max_length=30,
        choices=EventType.choices,
        help_text="Тип события"
    )
    raw_data = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "Первичные данные от контроллера (JSON). "
            "Содержит все сырые поля, включая внутренний ID события, "
            "коды ошибок и метки времени устройства. "
            "Используется для аудита, отладки и повторной обработки. "
        )
    )
    received_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Серверное время события"
        )
    processing_status = models.CharField(
        max_length=20,
        choices=ProcessStatus.choices,
        default=ProcessStatus.PENDING,
        help_text="Статус обработки события"
    )
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Время завершения обработки"
    )
    processing_error = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        help_text="Поле для записи ошибок внешнего элемента"
        )
    attempts = models.PositiveSmallIntegerField(
        default=0,
        help_text="Количество попыток обработки"
    )

    class Meta:
        verbose_name = "Событие внешнего элемента"
        verbose_name_plural = "События внешних элементов"
        ordering = ('-received_at',)
        indexes = [
            models.Index(fields=['controller', 'received_at'],
                         name="event_cntrl_received_idx"),
            models.Index(fields=['processing_status',],
                         name="processing_status_idx")
            ]

    def __str__(self) -> str:
        return f"{self.event_type} - {self.id} - {self.processing_status} - {self.controller} - {self.channel}"
