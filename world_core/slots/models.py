from django.db import models
from stations import Station, Controller

class Slot(models.Model):
    '''
    Модель Ячейка.
    Единица хранения арендуемых предметов.
    Одна ячейка в моменте может быть связана только с одним Предметом.
    '''
    class Status(models.TextChoices):
        EMPTY = ('empty', 'Свободна')
        BUSY = ('busy', 'Занята')

    slot_number = models.IntegerField() # поменять на Choice?
    w_slot_coordinates = models.IntegerField() 
    h_slot_coordinate = models.IntegerField()
    slot_status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.EMPTY
        )
    station = models.ForeignKey('stations.Station')
    controller = models.ForeignKey('stations.Controller')
    
