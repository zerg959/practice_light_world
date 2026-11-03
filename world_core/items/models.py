from django.db import models

class Item(models.Model):
    '''
    Модель Предмет.
    Для создания объектов Аренды.
    Связана с Ячейкой и Пользователем отношениями Unique-Constrait:
    Один Предмет может находиться только в одной Ячейке.
    Один Предмет в единицу времени может взять только один Пользователь.
    '''
    name = models.CharField()
    image = models.CharField()
    description = models.TextField(
        max_length=250,
        null=True,
        blank=True
    )
    complectation = models.CharField()
    weight = models.DecimalField(decimal_places=2)
    height = models.DecimalField(decimal_places=2)
    width = models.DecimalField(decimal_places=2)
