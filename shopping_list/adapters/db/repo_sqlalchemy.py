from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder  # that's ugly to have API framework dependency in here
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models, model_base
from shopping_list.domain import models as domain

DomainModelType = TypeVar("DomainModelType", bound=BaseModel)
DbModelType = TypeVar("DbModelType", bound=model_base.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseSqlAlchemyRepo(Generic[DomainModelType, DbModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, db_model: Type[DbModelType], domain_model: Type[DomainModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.db_model = db_model
        self.domain_model = domain_model

    def get(self, db: Session, id: Any) -> Optional[DomainModelType]:
        return self.domain_model.from_orm(db.query(self.db_model).filter(self.db_model.id == id).first())

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[DomainModelType]:
        return [self.domain_model.from_orm(obj) for obj in db.query(self.db_model).offset(skip).limit(limit).all()]

    def add(self, db: Session, *, obj_in: CreateSchemaType) -> DomainModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.db_model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return self.domain_model.from_orm(db_obj)

    def update(
            self,
            db: Session,
            *,
            db_obj: DbModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> DomainModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return self.domain_model.from_orm(db_obj)

    def remove(self, db: Session, *, id: Any) -> DomainModelType:
        obj = db.query(self.db_model).get(id)
        db.delete(obj)
        db.commit()
        return self.domain_model.from_orm(obj)

    def remove_all(self, db: Session):
        for obj in db.query(self.db_model).all():
            db.delete(obj)
        db.commit()

    def count(self, db: Session) -> int:
        return db.query(self.db_model).count()


class ShoppingList(BaseSqlAlchemyRepo[
                       domain.ShoppingList, models.ShoppingList, domain.ShoppingList, domain.ShoppingList]):
    pass


class Fridge(BaseSqlAlchemyRepo[domain.Fridge, models.Fridge, domain.Fridge, domain.Fridge]):
    pass


class Recipe(BaseSqlAlchemyRepo[domain.Recipe, models.Recipe, domain.Recipe, domain.Recipe]):
    pass


shopping_list = ShoppingList(models.ShoppingList, domain.ShoppingList)
fridge = Fridge(models.Fridge, domain.Fridge)
recipe = Recipe(models.Recipe, domain.Recipe)
