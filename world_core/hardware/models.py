from django.db import models
from django.core.validators import (MinValueValidator, MaxValueValidator)
from django.utils import timezone

class HardwareCommand(models.Model):
    '''
    Модель описывает очередь исходящих команд.
    Слой коммуникации для реализации физических действий, поступающих от/к Контроллера.
    Открыть - закрыть ячейку.
    Получить - отправить команду на Контроллер.
    '''

    class CommandType(models.TextChoices):
        OPEN_LOCK = ('open_lock', 'Открыть замок')
        GET_STATUS = ('get_status', 'Уточнить статус')
        REBOOT = ('reboot', 'Перезагрузить')
        PING = ('ping', 'Установить связь')

    class Status(models.TextChoices):
        PENDING = ('pending', 'Проверка')
        SENT = ('sent', 'Отправлено')
        ACKED = ('acked', 'Подтверждено')
        FAILED = ('failed', 'Неудачно') 
        TIMEOUT = ('timeout', 'Таймаут')
        CANCELLED = ('cancelled', 'Отменено')
        

    id = models.UUIDField()
    controller = models.ForeignKey('stations.Controller')
    channel = models.IntegerField(
        MinValueValidator(1),
        MaxValueValidator(16)
        )
    command_type = models.CharField(
        max_length=15,
        choices=CommandType.choices,
        default=CommandType.GET_STATUS
        )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING
    )


class SensorEvent(models.Model):
    '''
    Журнал входящих событий (raw data) от Контроллера
    '''
    class EventType(models.TextChoices):
        DOOR_OPEN = ('door_open', 'Дверь открыта')
        DOOR_CLOSE = ('door_close', 'Дверь закрыта')
        REBOOT = ('reboot', 'Перезагрузить')
        ERROR = ('error', 'Ошибка')

    id = models.UUIDField()
    controller = models.ForeignKey('stations.Controller')
    channel = models.IntegerField(
        MinValueValidator(1),
        MaxValueValidator(16),
        null=True,
        blank=True
        )
    raw_data = models.JSONField() # вся первичная дата от контроллера
    received_at = models.DateTimeField(default=timezone.now) # серверное время данных
    processed = models.BooleanField(default=False) # если повторная обработка не удалась
    processing_error = models.TextField(max_length=1000, null=True, blank=True) # поля для записи данных ошибки, если есть
