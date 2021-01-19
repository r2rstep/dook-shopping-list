from sqlalchemy import Column, Integer, String, JSON, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

from .model_base import Base


class Recipe(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    ingredients = Column(JSON)
    version_id = Column(Integer, nullable=False)

    __mapper_args__ = {
        "version_id_col": version_id
    }


class Fridge(Base):
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, index=True, nullable=False)
    products = Column(JSON)
    shopping_lists = relationship('ShoppingList', back_populates='fridge')
    version_id = Column(Integer, nullable=False)

    __mapper_args__ = {
        "version_id_col": version_id
    }


class ShoppingList(Base):
    id = Column(Integer, primary_key=True)
    items = Column(JSON)
    fridge_id = Column(Integer, ForeignKey('fridge.id'))
    fridge = relationship('Fridge', back_populates='shopping_lists')
    version_id = Column(Integer, nullable=False)

    __mapper_args__ = {
        "version_id_col": version_id
    }
