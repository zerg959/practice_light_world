from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from django.conf import settings


class Rental(models.Model):
    '''
    Модель для создания объекта Аренды.


    В Meta ключевые Constrints:
    Constraint 1:
    Cогласованность пары возврата:
    (return_slot пусто И return_station пусто)
    ИЛИ
    (return_slot заполнено И return_station заполнено).
    Constraint 2:
    Согласованность со статусом:
    статус «активна»  → return_slot и return_station пусты
    статус «завершена»/«отменена» → пара возврата заполнена

    '''
    class RentalUnit(models.TextChoices):
        """
        Доступные единицы аренды.
        """
        HOUR = ('hour', 'Час')
        DAY = ('day', 'Сутки')
        MONTH = ('month', 'Месяц')

    class RentalStatus(models.TextChoices):
        """
        Доступные статусы аренды.
        """
        FINISHED = ('finished', 'Завершена')
        STARTED = ('started', 'Начата')
        CANCELLED = ('cancelled', 'Отменена') 
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="UUID",
        help_text="Уникальный ID объекта аренды"
    )
    start_station = models.ForeignKey(
        'stations.Station',
        on_delete=models.PROTECT,
        related_name="started_rentals",
        verbose_name="Станция выдачи",
        help_text="Станция, где аренда началась"
        )
    start_slot = models.ForeignKey(
        'slots.Slot',
        on_delete=models.PROTECT,
        related_name="started_rentals",
        verbose_name="Ячейка выдачи",
        help_text="Ячейка, где аренда началась"
        )
    finish_station = models.ForeignKey(
        'stations.Station',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="finished_rentals",
        verbose_name="Станция возврата",
        help_text="Станция, где аренда завершилась"
        )
    finish_slot = models.ForeignKey(
        'slots.Slot',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="finished_rentals",
        verbose_name="Ячейка возврата",
        help_text="Ячейка, где аренда завершилась"
        )

    item = models.ForeignKey(
        'items.Item',
        on_delete=models.PROTECT,
        related_name="rentals",
        verbose_name="Предмет аренды",
        help_text="Предмет, взятый в аренду"
        )
    tariff = models.ForeignKey(
        'tariffs.Tariff',
        on_delete=models.PROTECT,
        related_name="rentals",
        verbose_name="Тариф",
        help_text="Тариф, примененный при начале аренды"
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="rentals",
        verbose_name="Клиент",
        help_text="Пользователь аренды",
        )
    rental_unit = models.CharField(
        max_length=15,
        choices=RentalUnit.choices,
        verbose_name="Единица времени аренды",
        help_text="Возможные единицы аренды"
    )
    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'), message="Ставка аренды не может быть меньше 0.01")],
        verbose_name="Ставка аренды",
        help_text="Ставка за единицу аренды"
        )
    rental_status = models.CharField(
        max_length=20,
        choices=RentalStatus.choices,
        default=RentalStatus.STARTED,
        verbose_name="Состояние аренды",
        help_text="Текущее состояние аренды"
    )
    rental_start = models.DateTimeField(
        null=False,
        verbose_name="Время начала аренды",
        help_text="Фиксируется сервисом при старте аренды"
        )
     # Проверку «конец > начало» лучше делать и в модели ((clean), и на фронтенде, и в сериализаторе DRF).
    rental_finish = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Время завершения аренды",
        help_text="Заполняется при закрытии аренды, остаётся пустым для активных"
        )

    class Meta:
        verbose_name = "Процесс аренды"
        verbose_name_plural = "Процессы аренды"
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(finish_slot__isnull=True, finish_station__isnull=True)
                    | models.Q(finish_slot__isnull=False, finish_station__isnull=False)
                ),
                name='rental_finish_pair_chk',
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(rental_status=RentalStatus.STARTED)
                    & models.Q(finish_slot__isnull=True, finish_station__isnull=True)
                )
                | (
                    ~models.Q(rental_status=RentalStatus.STARTED)
                & models.Q(finish_slot__isnull=False, finish_station__isnull=False)
                ),
                name='rental_status_finish_chk',
            ),
            
            models.UniqueConstraint(
                fields=['start_slot'],
                condition=models.Q(rental_status=RentalStatus.STARTED),
                name='uniq_active_rental_slot',          # имя короче 30!
            ),
            models.UniqueConstraint(
                fields=['item'],
                condition=models.Q(rental_status=RentalStatus.STARTED),
                name='uniq_active_rental_item',
            ),
        ]

    def __str__(self) -> str:
        return f"Аренда {self.id}, станция: {self.start_station_id}, ячейка {self.start_slot_id}, статус {self.rental_status}"

    def clean(self):
        # Проверку «конец > начало» лучше делать и в модели ((clean), и на фронтенде, и в сериализаторе DRF).
            pass


class RentalEvent(models.Model):
    """
    Неизменяемая история аренды.
    Каждое событие фиксирует факт и цифры на момент его совершения.
    Записи не редактируются и не удаляются.
    """

    class EventType(models.TextChoices):
        STARTED = ('started', 'Старт')
        FINISHED = ('finished', 'Завершение')
        CANCELLED = ('cancelled', 'Отмена')

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="UUID",
        help_text="Уникальный ID события",
    )
    rental = models.ForeignKey(
        'rentals.Rental',
        on_delete=models.PROTECT,
        related_name="events",
        verbose_name="Аренда",
        help_text="Аренда, к которой относится событие",
    )
    type = models.CharField(
        max_length=20,
        choices=EventType.choices,
        verbose_name="Тип события",
        help_text="Какое событие произошло",
    )

    started_at = models.DateTimeField(
        verbose_name="Начало события",
        help_text="Момент начала периода события (для 'старта' — старт аренды)",
    )
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Конец события",
        help_text="Заполняется для 'завершения', пуст для 'старта' и 'отмены'",
    )

    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за единицу",
        help_text="Снапшот цены на момент события",
    )
    unit = models.CharField(
        max_length=15,
        verbose_name="Единица расчёта",
        help_text="Снапшот единицы аренды на момент события",
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Итоговая сумма",
        help_text="Обязательна для 'завершения', пуста для остальных событий",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rental_events",
        verbose_name="Инициатор",
        help_text="Кто инициировал событие (система — NULL)",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания записи",
        help_text="Момент записи события в базу",
    )

    @classmethod
    def log(cls, *, rental, event_type, started_at, finished_at=None,
            total_amount=None, created_by=None):
        """
        Единственная точка создания событий.
        Снапшоты цифры берёт сам — из Rental, в момент вызова.
        """
        return cls.objects.create(
            rental=rental,
            type=event_type,
            started_at=started_at,
            finished_at=finished_at,
            price_per_unit=rental.price_per_unit,   # копия значения из Rental
            unit=rental.rental_unit,                # копия значения из Rental
            total_amount=total_amount,
            created_by=created_by,
        )

    class Meta:
        verbose_name = "Событие аренды"
        verbose_name_plural = "События аренды"
        ordering = ["started_at", "created_at"]
        indexes = [
            models.Index(fields=["rental", "started_at"]),
        ]

    def __str__(self):
        return f"{self.get_type_display()} аренды {self.rental_id} от {self.started_at:%d.%m.%Y %H:%M}"