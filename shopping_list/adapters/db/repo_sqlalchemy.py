from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder   # that's ugly to have API framework dependency in here
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models, model_base
from shopping_list.domain import models as domain


ModelType = TypeVar("ModelType", bound=model_base.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseSqlAlchemyRepo(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def add(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
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
        return db_obj

    def remove(self, db: Session, *, id: Any) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def remove_all(self, db: Session):
        for obj in db.query(self.model).all():
            db.delete(obj)
        db.commit()

    def count(self, db: Session):
        return db.query(self.model).count()


class ShoppingList(BaseSqlAlchemyRepo[models.ShoppingList, domain.ShoppingListLogic, domain.ShoppingListLogic]):
    pass


class Fridge(BaseSqlAlchemyRepo[models.Fridge, domain.Fridge, domain.Fridge]):
    pass


class Recipe(BaseSqlAlchemyRepo[models.Fridge, domain.Fridge, domain.Fridge]):
    pass


shopping_list = ShoppingList(models.ShoppingList)
fridge = Fridge(models.Fridge)
recipe = Recipe(models.Recipe)
