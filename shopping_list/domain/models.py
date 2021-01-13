import enum
from typing import List, Dict

import attr
from pydantic import BaseModel


class QuantityUnits(enum.IntEnum):
    units = enum.auto()
    gram = enum.auto()


class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: QuantityUnits


class IngredientInFridge(Ingredient):
    allocated_quantity: float = 0.0


class Recipe(BaseModel):
    ingredients: List[Ingredient]


@attr.s
class ShoppingList:
    _ingredients_in_fridge: List[IngredientInFridge] = attr.ib()
    items: Dict[str, float] = attr.ib(factory=dict)

    def create(self, recipes: List[Recipe]):
        for recipe in recipes:
            for ingredient_in_recipe in recipe.ingredients:
                try:
                    ingredient_in_fridge = next(
                        filter(lambda in_fridge: in_fridge.name == ingredient_in_recipe.name,
                               self._ingredients_in_fridge))
                    quantity_to_buy = ingredient_in_recipe.quantity - ingredient_in_fridge.quantity
                    # neglect possible mismatch of units for now
                    if ingredient_in_fridge.quantity < ingredient_in_recipe.quantity:
                        if ingredient_in_recipe.name not in self.items:
                            self.items[ingredient_in_recipe.name] = quantity_to_buy
                        else:
                            self.items[ingredient_in_recipe.name] += quantity_to_buy
                    ingredient_in_fridge.allocated_quantity = \
                        ingredient_in_fridge.quantity if quantity_to_buy >= 0 else ingredient_in_recipe.quantity
                except StopIteration:
                    self.items[ingredient_in_recipe.name] = ingredient_in_recipe.quantity
