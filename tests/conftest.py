import pytest
from sqlalchemy.orm import Session

from shopping_list.adapters import db as _db
from shopping_list.bootstrap import bootstrap


@pytest.fixture
def db() -> Session:
    bootstrap()
    yield _db.session.Session()
