from django.db import models
from django.core.validators import (MinValueValidator, MaxValueValidator)


class Slot(models.Model):
    '''
    Модель Ячейка.
    Единица хранения арендуемых предметов.
    Одна Ячейка в моменте может быть связана только с одним Предметом.
    Одна Ячейка управляется одним Каналом Контроллера.
    Уникальность связи реализована в Meta.constraints модели.
    ВАЖНО:
    Прямая привязка Ячейка - Станция в модели отсутствует.
    Станция и Ячейка связаны только через модель Контроллер.
    '''
    class Status(models.TextChoices):
        """
        Возможные статусы Ячейки.
        """
        EMPTY = ('empty', 'Свободна')
        BUSY = ('busy', 'Занята')

    class SlotWidth(models.IntegerChoices):
        """
        Высота Ячейки: возможные габариты.
        """
        w_XSMALL = 10, "10 см"
        w_SMALL = 20, "20 см"
        w_MEDIUM = 40, "40 см"
        w_LARGE = 100, "100 см"

    class SlotHeight(models.IntegerChoices):
        """
        Ширина Ячейки: возможные габариты.
        """
        h_SMALL = 30, "30 см"
        h_MEDIUM = 40, "40 см"
        h_LARGE = 60, "60 см"

    slot_number = models.PositiveSmallIntegerField(
        max_length=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1, message="Номер Ячейки не должен быть меньше 1"),
            MaxValueValidator(16, message="Номер кЯчейки не может быть больше 16")
        ],
        verbose_name="Номер Ячейки",
        help_text="Номер Ячейки в Станции"
    ) # поменять на Choice?

    width = models.CharField(
        max_length=3,
        choices=SlotWidth.choices,
        null=True,
        blank=True,
        default=None,
        verbose_name="Высота ячейки, см",
        help_text="Выбор габарита ячейки по высоте (см)"
    )
    height = models.CharField(
        max_length=3,
        choices=SlotHeight.choices,
        null=True,
        blank=True,
        default=None,
        verbose_name="Ширина ячейки, см",
        help_text="Выбор габарита ячейки по ширине (см)"
    )
    slot_status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.EMPTY,
        verbose_name="Статус ячейки",
        help_text="Актуальный статус ячейки"
        )
    controller = models.ForeignKey(
        'stations.Controller',
        on_delete=models.CASCADE,
        related_name="slots",
        null=True,
        blank=True,
        verbose_name="Контроллер станции",
        help_text="Контроллер станции, в которой расположена ячейка"
        )
    controller_channel_num = models.PositiveSmallIntegerField(
        max_length=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1, message="Номер канала не должен быть меньше 1"),
            MaxValueValidator(16, message="Номер канала не должен быть больше 16")
        ],
        verbose_name="Номер канала",
        help_text="Номер канала, через который Контроллер управляет Ячейкой"
    )

    class Meta:
        verbose_name = "Ячейка"
        verbose_name_plural = "Ячейки"
        constraints = [
            models.UniqueConstraint(
                fields=['controller', 'controller_channel_num'],
                name="unique_cntrl_chnl_per_slot")
                ]

    def __str__(self) -> str:
        if self.controller and self.controller.station_id:
            return f"Ячейка {self.id} (канал {self.channel_number}, станция {self.controller.station_id})"
        return f"Ячейка {self.id} (не подключена)"
