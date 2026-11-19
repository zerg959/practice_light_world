import pytest
from django.utils import timezone
from datetime import timedelta
from rentals.models import (
    Rental, RentalEvent, EventType, 
    RentalStatus
    )


RENTAL_START = timezone.make_aware(
    timezone.datetime(2026, 10, 15, 10, 0, 0)
)
RENTAL_FINISH = RENTAL_START + timedelta(hours=2)
RENTAL_HOURS = 2

@pytest.fixture
def started_rental(station, busy_slot, available_item, active_tariff, user):
    """
    Аренда в статусе "Начата" - фикстура -модель Rental
    Предмет забирается из занятого слота
    Price_per_unit и rental_unit берутся из FK-Tariff (снапшот на момент старта)
    rental_start задается в константе RENTAL_START
    """
    started_rental = Rental.objects.create(
        start_station=station,
        start_slot=busy_slot,
        item=available_item,
        tariff=active_tariff,
        user=user,
        rental_unit=active_tariff.unit,
        price_per_unit=active_tariff.price_per_unit,
        rental_start=RENTAL_START
    )
    return started_rental


@pytest.fixture
def finished_rental(station, busy_slot, empty_slot, available_item, active_tariff, user):
    """
    Аренда в статусе "Завершена" - фикстура - модель Rental
    Предмет возвращен в пустой слот
    Price_per_unit и rental_unit берутся из FK-Tariff (снапшот на момент старта)
    rental_start задается в константе RENTAL_START
    rental_finish - в RENTAL_FINISH
    """
    finished_rental = Rental.objects.create(
        start_station=station,
        finish_station=station,
        start_slot=busy_slot,
        finish_slot=empty_slot,
        item=available_item,
        tariff=active_tariff,
        user=user,
        rental_unit=active_tariff.unit,
        price_per_unit=active_tariff.price_per_unit,
        rental_status=RentalStatus.FINISHED,
        rental_start=RENTAL_START,
        rental_finish=RENTAL_FINISH,
    )
    return finished_rental

@pytest.fixture
def started_rental_event(started_rental):
    """
    Событие-снапшот Аренды со статусом "Начата" - RentalEvent.
    В фикстуре еще нет времени завершения.
    Фиксирует состояние экземпляра Rental в моменте старта
    используя метод log().
    """
    return RentalEvent.log(
        rental=started_rental,
        type=EventType.STARTED,
        created_at=started_rental.rental_start
    )

@pytest.fixture
def finished_rental_event(finished_rental):
    """
    Событие-снапшот Аренды со статусом "Завершена" - RentalEvent.
    Фиксирует состояние экземпляра Rental в моменте финиша,
    используя метод log()
    Время окончания и начала взяты из конфтест-констант.
    """
    return RentalEvent.log(
        rental=finished_rental,
        type=EventType.FINISHED,
        total_amount=finished_rental.price_per_unit * RENTAL_HOURS,
    )