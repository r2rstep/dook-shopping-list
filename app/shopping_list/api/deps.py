from typing import Generator

from ..adapters.db.session import Session


def get_db() -> Generator:
    db = Session()
    try:
        yield db
    finally:
        db.close()
