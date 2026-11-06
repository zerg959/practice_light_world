import pytest
from stations.models import Station, StationConfig, Controller


@pytest.mark.django_db
class TestStationModel:
    """
    Юнит-тесты модели Statiion (Станция).
    """
    def test_station_created(self, station):
        """
        Станция создается в БД.
        Станция доступна по ID.
        Станция содержит информацию о расположении.
        """
        found = Station.objects.filter(id=station.id).first()
        assert found is not None
        assert found.location == station.location
