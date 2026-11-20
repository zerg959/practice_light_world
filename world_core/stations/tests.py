import pytest
from django.db import IntegrityError
from stations.models import (
    Station, StationConfig, Controller, 
    StationStatus, ConfigStatus, ControllerStatus
    )


@pytest.mark.django_db
class TestStationModel:
    """
    Юнит-тесты модели Station (Станция).
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

    def test_correct_default_station_status(self, station):
        """
        Станция содержит корректный дефолтный статус
        """
        assert station.station_status == StationStatus.OFFLINE


@pytest.mark.django_db
class TestStationConfigModel:
    """
    Юнит-тесты модели Конфигурация Станции (StationConfig)
    """
    def test_config_created_in_db(self, station_config):
        """
        Конфиг Станции создаётся в БД.
        Конфиг доступен по ID.
        Конфиг имеет номер версии.
        Статус Конфига по умолчанию сохраняется верно.
        Снапшот конфига по умолчанию является пустым Dict.
        """
        found = StationConfig.objects.filter(id=station_config.id).first()
        assert found is not None
        assert found.id == station_config.id
        assert found.version_number == station_config.version_number
        assert found.status == ConfigStatus.PUBLISHED
        assert found.snapshot == {}

@pytest.mark.django_db
class TestControllerModel:
    """
    Юнит-тесты класса Контроллер (Controller)
    """
    def test_controller_created_id_db(self, controller):
        """
        Контроллер создается в БД.
        Контроллер доступен по ID.
        Контроллер связан с указанной Станцией.
        Контроллер имеет имя.
        Контроллер имеет serial_number.
        Контроллер имеет корректный статус по умолчанию.
        """
        found = Controller.objects.filter(pk=controller.pk).first()
        assert found is not None
        assert found.id == controller.id
        assert found.station_id == controller.station.id
        assert found.name == controller.name
        assert found.serial_number == controller.serial_number
        assert found.status == ControllerStatus.OFFLINE

    def test_controller_serial_num_is_unique(self, station, controller):
        
        """
        При создании Контроллера с таким же serial number выводится ошибка.
        """
        with pytest.raises(IntegrityError):
            Controller.objects.create(
                station=station,
                serial_number=controller.serial_number
            )
