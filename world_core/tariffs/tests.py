import pytest
from tariffs.models import Tariff, TariffUnit

@pytest.mark.django_db

class TestTariffModel:
    """
    Юнит-тесты модели Tariff.
    """
    def test_tariff_created_in_db(self, active_tariff):
        """Созданный тариф сохраняется в БД c корректными необязательными атрибутами"""
        found = Tariff.objects.filter(id=active_tariff.id).first()
        assert found is not None
        assert found.id == active_tariff.id
        assert found.price_per_unit == active_tariff.price_per_unit
        assert found.unit == active_tariff.unit
    
    def test_tariff_default_is_active(self, active_tariff):
        """Созданный тариф по умолчанию с активным флагом "Действующий"""
        assert active_tariff.is_active is True

    def test_tariff_is_active_false(self, inactive_tariff):
        """У неактивного тарифа сохраняется неактивный флаг "Действующий"""
        assert inactive_tariff.is_active is False