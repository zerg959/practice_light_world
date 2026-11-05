from django.db import models
import uuid


class Item(models.Model):
    '''
    Модель Предмет.
    Для создания объектов Аренды.
    Связь с ячейкой и пользователем реализуется через модель Аренды/Размещения,
    Единственность актуальной связи обеспечивает условный констрейнт
    Один Предмет может находиться только в одной Ячейке.
    Один Предмет в единицу времени может взять только один Пользователь.
    '''
    class Status(models.TextChoices):
        """
        Статусы предмета.
        """
        AVAILABLE = ('available', 'Доступен')
        RENTED = ('rented', 'В аренде')
        MAINTENANCE = ('maintenance', 'На обслуживании')
        RETIRED = ('retired', 'Списан')

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="UUID",
        help_text="Уникальный ID предмета",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
        help_text="Наименование Предмета"
    )
    image = models.CharField( # пока храним как ссылку
        max_length=2000,
        null=True,
        blank=True,
        verbose_name="Фото",
        help_text="Изображение предмета"
    )
    description = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Описание предмета",
        help_text="Описание"
    )
    equipment = models.TextField(
        blank=True,
        verbose_name="Комплектация",
        help_text="Перечень оборудования, входящего в аренду"
    )
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Вес",
        help_text="Вес комплектации в кг"
        )
    height = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Высота",
        help_text="Высота в см"
        )
    width = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Ширина",
        help_text="Ширина в см"
        )
    current_slot = models.ForeignKey(
        'slots.Slot',
        on_delete=models.PROTECT,
        related_name="items",
        null=True,
        blank=True,
        verbose_name="Текущая ячейка",
        help_text=(
            "Ячейка, в которой предмет находится сейчас. "
            "Пусто, когда предмет у арендатора"
        ),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        verbose_name="Статус",
        help_text="Текущий статус предмета",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата создания"
    )

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ('-created_at', 'name')
        indexes = [
            models.Index(fields=['created_at', 'name'],
                         name='item_created_name_idx'),
            models.Index(fields=['name'], name='item_name_idx'),
            models.Index(fields=['status', 'current_slot'],
                         name='item_status_slot_idx'),
        ]

    def __str__(self) -> str:
        return f"Предмет {self.name} - ID {self.id}"
