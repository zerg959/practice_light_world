from django.db import models


class Item(models.Model):
    '''
    Модель Предмет.
    Для создания объектов Аренды.
    Связь с ячейкой и пользователем реализуется через модель Аренды/Размещения,
    Единственность актуальной связи обеспечивает условный констрейнт
    Один Предмет может находиться только в одной Ячейке.
    Один Предмет в единицу времени может взять только один Пользователь.
    '''
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
                         name='created_at_name_idx'),
            models.Index(fields=['name',], name='name_idx')
        ]

    def __str__(self) -> str:
        return f"Предмет {self.name} - ID {self.id}"
