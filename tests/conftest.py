import pytest
from sqlalchemy.orm import Session

from shopping_list.adapters import db as _db


@pytest.fixture
def db() -> Session:
    _db.model_base.Base.metadata.create_all(bind=_db.session.engine)
    yield _db.session.session()
