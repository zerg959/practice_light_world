# global test fixtures (auth, time, DB)
import pytest
from faker import Faker
from pytest_mock import MockerFixture
from decimal import Decimal

from users.models import User, Role
from hardware.models import HardwareCommand, CommandStatus, CommandType, SensorEvent, ProcessStatus
from items.models import Item, ItemStatus
from rentals.models import Rental, RentalEvent, RentalStatus, RentalUnit
from slots.models import Slot, SlotStatus, SlotWidth, SlotHeight
from stations.models import Station, StationConfig, StationStatus, Controller, ConfigStatus, ControllerStatus
from tariffs.models import Tariff, TariffUnit

@pytest.fixture
def fake():
    """
    Faker фикстура.
    """
    return Faker (locale="ru_RU")
 

@pytest.fixture
def user(fake):
    """
    Фикстура Пользователь
    """
    user = User.objects.create(
        username=fake.user_name(),
        email=fake.email(),
        role=Role.USER
    )
    return user


@pytest.fixture
def admin(fake):
    """
    Фикстура Администратор
    """
    admin = User.objects.create(
        username=fake.user_name(),
        email=fake.email(),
        role=Role.ADMIN
    )
    return admin

@pytest.fixture
def station(fake):
    """
    Станция - фикстура.
    """
    station = Station.objects.create(
        location=fake.city()
    )
    return station


@pytest.fixture
def station_config():
    """
    Конфиг Станции - фикстура.
    """
    return StationConfig.objects.create(
        version_number=Decimal("1"),
    )

@pytest.fixture
def controller(fake, station):
    """
    Контроллер - фикстура
    """
    controller = Controller.objects.create(
        name=fake.bothify(text="CTRL-##-??"),
        serial_number=fake.uuid4(),
        station=station,
        status=ControllerStatus.OFFLINE
    )
    return controller

@pytest.fixture
def active_tariff(fake):
    """
    Активный Тариф - фикстура
    """
    active_tariff = Tariff.objects.create(
        unit=TariffUnit.HOUR,
        price_per_unit=Decimal("1.00"),
        version="2026-beta"
    )
    return active_tariff

@pytest.fixture
def inactive_tariff(fake):
    """
    Наактивный Тариф - фикстура
    """
    inactive_tariff = Tariff.objects.create(
        unit=TariffUnit.HOUR,
        price_per_unit=Decimal("1.50"),
        version="2025-old",
        is_active=False
    )
    return inactive_tariff