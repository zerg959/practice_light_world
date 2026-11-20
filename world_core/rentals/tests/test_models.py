import pytest
from .constants import RENTAL_FINISH, RENTAL_HOURS, RENTAL_START

from rentals.models import Rental, RentalEvent, RentalStatus, RentalUnit, EventType


@pytest.mark.django_db
class TestRentalModel:
    """
    Юнит-тесты класса Rent (Аренда).
    """
    def test_rental_created_in_db_in_started_status(self, started_rental):
        """
        Аренда создается в БД.

        Аренда создается с корректным статусом.
        """
        found = Rental.objects.filter(id=started_rental.id).first()
        assert found is not None
        assert found.id == started_rental.id
        assert found.rental_status == RentalStatus.STARTED

    def test_rental_created_snapshots_of_tariff(self, started_rental, active_tariff):
        """
        Аренда копирует параметры из активного Тарифа.
        """
        found = Rental.objects.filter(id=started_rental.id).first()
        assert found.price_per_unit == active_tariff.price_per_unit
        assert found.rental_unit == active_tariff.unit



@pytest.mark.django_db
class TestRentalEventModel:
    """
    Юнит-тесты класса RentalEvent (Событие Аренды)
    """
    def test_started_rental_event_created_in_db(self, started_rental_event):
        """
        Снапшот начатой Аренды успешно создаётся в БД.
        """
        found = RentalEvent.objects.filter(id=started_rental_event.id).first()
        assert found is not None
        assert found.id == started_rental_event.id

    def test_started_rental_event_has_correct_data(self, started_rental, active_tariff, started_rental_event):
        """
        Данные из аренды со статусом "Начата" успешно фиксируются в экземпляре СобытиеАренды
        """
        found = RentalEvent.objects.filter(id=started_rental_event.id).first()
        assert found.price_per_unit == active_tariff.price_per_unit
        assert found.rental.id == started_rental.id
        assert found.event_type == EventType.STARTED
        assert found.started_at == started_rental.rental_start
        assert found.finished_at is None
        assert found.unit == active_tariff.unit
        assert found.total_amount is None