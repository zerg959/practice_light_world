# global test fixtures (auth, time, DB)
import pytest
from faker import Faker
from pytest_mock import MockerFixture


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
def station_config(station, admin):
    """
    Конфиг Станции - фикстура.
    """
    station_config = StationConfig.objects.create(
        version_number=5,
        station=station,
        created_by=admin
    )
    return  station_config

@pytest.fixture
def controller(fake, station):
    """
    Контроллер - фикстура
    """
    controller = Controller.objects.create(
        name = fake.bothify(text="CTRL-##-??"),
        serial_number = fake.uuid4(),
        station=station,
        status=ControllerStatus.OFFLINE
    )
    return controller
