from sqlalchemy import Column, Integer, String, JSON

from .model_base import Base


class Recipe(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    ingredients = Column(JSON)


class Fridge(Base):
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, index=True)
    products = Column(JSON)


class ShoppingList(Base):
    id = Column(Integer, primary_key=True)
    items = Column(JSON)
