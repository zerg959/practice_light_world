from django.db import models
from stations import Station
from slots import Slot
from users import User
from tariffs import Tariff
from items import Item

class Rental(models.Model):
    '''
    Модель для создания объекта Аренды
    '''
    id = models.UUIDField()
    station = models.ForeignKey('stations.Station')
    slot = models.ForeignKey('slots.Slot')
    item = models.ForeignKey('items.Item')
    tariff = models.ForeignKey('tariffs.Tariff')
    user = models.ForeignKey('users.User')
    


class RentalEvent(models.Model):
    '''
    Модель для хранения событий реализованных Аренд,
    необходима для хранения неизменяемых исторических данных
    '''
    rental = models.ForeignKey('rentals.Rental')
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField()