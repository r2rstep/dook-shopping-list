from typing import List

from pydantic import BaseModel

from .fridge import ProductInFridge


class CreateShoppingList(BaseModel):
    recipes: List[int]


class ChangeFridgeContents(BaseModel):
    products: List[ProductInFridge]
