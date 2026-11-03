from django.db import models


class Tariff(models.Model):
    '''
    Модель Тариф.
    '''
    unit = models.CharField()
    price_per_unit = models.DecimalField(decimal_places=2)
    version = models.CharField()