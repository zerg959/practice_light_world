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
        help_text="Наименование Предмета"
    )
    image = models.CharField( # пока храним как ссылку
        max_length=2000,
        null=True,
        blank=True,
        help_text="Картинка"
    )
    description = models.CharField(
        max_length=250,
        blank=True,
        help_text="Описание"
    )
    equipment = models.TextField(
        blank=True,
        help_text="Комплектация"
    )
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Вес, кг"
        )
    height = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Высота, см"
        )
    width = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ширина, см"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
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
