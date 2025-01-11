import pytest
import pytest_asyncio
from starlette.testclient import TestClient
from tortoise import Tortoise

from src.run import app


@pytest.fixture
def client_app():
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
