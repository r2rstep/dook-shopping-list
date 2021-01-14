from fastapi.encoders import jsonable_encoder       # that's ugly to have API framework dependency in here
from sqlalchemy.orm import Session

from . import models
from .repository_base import AbstractRepository
from shopping_list.domain import models as domain


class ShoppingList(AbstractRepository):
    def __init__(self, session: Session):
        self._session: Session = session

    def add(self, obj: domain.ShoppingList) -> int:
        pass

    def get(self, id: int) -> domain.ShoppingList:
        pass


class Fridge(AbstractRepository):
    def __init__(self, session: Session):
        self._session: Session = session

    def add(self, obj: domain.Fridge) -> int:
        pass

    def get(self, id: int) -> domain.Fridge:
        pass


class Recipe(AbstractRepository):
    def __init__(self, session: Session):
        self._session: Session = session

    def add(self, obj: domain.Recipe) -> domain.Recipe:
        obj_in_data = jsonable_encoder(obj)
        db_obj = models.Recipe(**obj_in_data)
        self._session.add(db_obj)
        self._session.commit()
        self._session.refresh(db_obj)
        return db_obj

    def get(self, id: int) -> domain.Recipe:
        pass
