from django.db import models
from slots import Slot


class Station(models.Model):
    '''
    Модель Станция.
    Содержит слоты для хранения объектов выдачи.
    '''
    class Status(models.TextChoices):
        ONLINE = ('online', 'Онлайн')
        OFFLINE = ('offline', 'Офлайн')
    slots = models.ForeignKey(
        'slots.Slot'
    )

    location = models.CharField() # заменить на координаты?
    current_applied_config_version = models.ForeignKey(
        'stations.StationConfig'
    )
    station_status = models.CharField(
        max_length=6,
        choices=Status.choices,
        default=Status.OFFLINE,
        verbose_name='Статус станции'
    )


class StationConfig(models.Model):
    '''
    Модель для хранения опубликованных(published), но не примененных 
    конфигураций станций.
    Используемые (applied) версии записываются в БД и применяются в поле
    current_applied_config.
    '''
    class Status(models.TextChoices):   # переименовать класс (в Станции тоже есть Статус)
        PUBLISHED = ('published', 'Опубликовано') 
        APPLIED = ('applied', 'Применено')
        DEPRECATED = ('deprecated', 'Устарело')

    station = models.ForeignKey('stations.Station')
    version_number = models.DecimalField()
    status = models.CharField(
        max_length=12,
    )
    snapshot = models.JSONField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания конфигурации'
    )
    created_by = models.ForeignKey()

    class Meta:
        verbose_name = 'Конфигурация'
        verbose_name_plural = 'Конфигурации'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'Версия: {self.version_number}, от {self.created_at}'
