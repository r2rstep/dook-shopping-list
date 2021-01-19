from sqlalchemy import Column, Integer, String, JSON, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

from .model_base import Base


class Recipe(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    ingredients = Column(JSON)


class Fridge(Base):
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, index=True)
    products = Column(JSON)
    shopping_lists = relationship('ShoppingList', back_populates='fridge')


class ShoppingList(Base):
    id = Column(Integer, primary_key=True)
    items = Column(JSON)
    fridge_id = Column(Integer, ForeignKey('fridge.id'))
    fridge = relationship('Fridge', back_populates='shopping_lists')
