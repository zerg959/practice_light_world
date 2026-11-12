import pytest
from tariffs.models import Tariff, TariffUnit

@pytest.mark.django_db
def test_tariff_created_in_db(self)