import pytest

from rentals.models import Rental, RentalEvent, RentalStatus, RentalUnit


@pytest.mark.django_db
class TestRentalModel:
    """
    Юнит-тесты класса Rent (Аренда)
    """
    def test_rental_created_in_db_in_started_status(self, started_rental):
        """
        Проверяем, что Аренда создается в БД с коректным статусом
        """
        found = Rental.objects.filter(id=started_rental.id).first()
        assert found is not None
        assert found.id == started_rental.id
        assert found.rental_status == RentalStatus.STARTED

    def test_rental_created_snapshots_of_tariff(self, started_rental, active_tariff):
        """
        Проверяем, что Аренда копирует параметры из активного Тарифа.
        """
        found = Rental.objects.filter(id=started_rental.id).first()
        assert found.price_per_unit == active_tariff.price_per_unit
        assert found.rental_unit == active_tariff.unit



@pytest.mark.django_db
class TestRentalEventModel:
    """
    Юнит-тесты класса RentalEvent (Событие Аренды)
    """
    pass