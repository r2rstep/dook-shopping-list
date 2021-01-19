from typing import List

from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    quantity: float

    class Config:
        orm_mode = True


class Recipe(BaseModel):
    id: int = None
    name: str
    ingredients: List[Ingredient]

    class Config:
        orm_mode = True
