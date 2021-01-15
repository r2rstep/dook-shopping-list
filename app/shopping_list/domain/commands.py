from typing import List

from pydantic import BaseModel


class CreateShoppingList(BaseModel):
    recipes: List[int]
