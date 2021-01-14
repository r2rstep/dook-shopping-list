import pytest

from shopping_list.adapters import db


@pytest.fixture(autouse=True)
def bootstrap():
    db.model_base.Base.metadata.create_all(bind=db.session.engine)
