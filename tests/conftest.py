import pytest
import pytest_asyncio
from starlette.testclient import TestClient
from tortoise import Tortoise

from src.run import app
from tests.factory_test import UserFactory


@pytest.fixture
def client_api():
    return TestClient(app)


@pytest_asyncio.fixture
async def mock_prepare_db():
    await Tortoise.init(
        db_url='sqlite://:memory:',
        modules={'models': ['src.models']},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.fixture
async def default_user_record_constructor():
    user = await UserFactory.build()
    await user.save()
    return user
