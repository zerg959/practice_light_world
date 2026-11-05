# global test fixtures (auth, time, DB)

import pytest
from faker import Faker
from pytest_mock import MockerFixture

@pytest.fixture
def fake():
    """
    Faker fixture.
    """
    return Faker()