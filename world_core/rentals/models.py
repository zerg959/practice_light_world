from django.db import models


class Rental(models.Model):
    '''
    Модель для создания объекта Аренды
    '''
    pass


class RentalEvent(models.Model):
    '''
    Модель для хранения событий реализованных Аренд,
    необходима для хранения неизменяемых исторических данных
    '''
    pass