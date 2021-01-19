from typing import Any, Dict, Generic, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder  # that's ugly to have API framework dependency in here
from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from . import models, model_base
from shopping_list.domain import fridge as fridge_models, shopping_list as shopping_list_models

DomainModelType = TypeVar("DomainModelType", bound=BaseModel)
DbModelType = TypeVar("DbModelType", bound=model_base.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class GenericSqlAlchemyRepo(Generic[DomainModelType, DbModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, db_model: Type[DbModelType], domain_model: Type[DomainModelType]):
        self.db_model = db_model
        self.domain_model = domain_model

    def get(self, db: Session, id: Any) -> (DbModelType, DomainModelType):
        db_obj = db.query(self.db_model).filter(self.db_model.id == id).first()
        domain_obj = self.domain_model.from_orm(db_obj)
        return db_obj, domain_obj

    def add(self, db: Session, *, obj_in: CreateSchemaType) -> (DbModelType, DomainModelType):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.db_model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj, self.domain_model.from_orm(db_obj)

    def update(
            self,
            db: Session,
            *,
            db_obj: DbModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> (DbModelType, DomainModelType):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        columns = [col.key for col in inspect(db_obj).mapper.column_attrs]
        for field in update_data:
            if field in columns:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj, self.domain_model.from_orm(db_obj)

    def remove(self, db: Session, *, id: Any) -> (DbModelType, DomainModelType):
        db_obj = db.query(self.db_model).get(id)
        db.delete(db_obj)
        db.commit()
        return db_obj, self.domain_model.from_orm(db_obj)

    def remove_all(self, db: Session):
        for obj in db.query(self.db_model).all():
            db.delete(obj)
        db.commit()

    def count(self, db: Session) -> int:
        return db.query(self.db_model).count()


class ShoppingList(GenericSqlAlchemyRepo[
                       shopping_list_models.ShoppingList,
                       models.ShoppingList,
                       shopping_list_models.ShoppingList,
                       shopping_list_models.ShoppingList]):
    pass


class Fridge(GenericSqlAlchemyRepo[fridge_models.Fridge, models.Fridge, fridge_models.Fridge, fridge_models.Fridge]):
    def get_with_shopping_lists(self, db: Session, id: Any) -> (DbModelType, DomainModelType):
        db_obj = db.query(self.db_model).\
            join(models.Fridge.shopping_lists).\
            filter(self.db_model.id == id).first()
        domain_obj = self.domain_model.from_orm(db_obj)
        return db_obj, domain_obj


class Recipe(GenericSqlAlchemyRepo[
                 shopping_list_models.Recipe, models.Recipe, shopping_list_models.Recipe, shopping_list_models.Recipe]):
    pass


shopping_list = ShoppingList(models.ShoppingList, shopping_list_models.ShoppingList)
fridge = Fridge(models.Fridge, fridge_models.Fridge)
recipe = Recipe(models.Recipe, shopping_list_models.Recipe)
