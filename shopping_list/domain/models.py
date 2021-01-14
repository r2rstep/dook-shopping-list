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


class ProductInFridge(Ingredient):
    allocated_quantity: float = 0.0


def set_allocated_quantity(ingredient_in_fridge: ProductInFridge, ingredient: Ingredient):
    ingredient_in_fridge.allocated_quantity += ingredient.quantity
    if ingredient_in_fridge.allocated_quantity > ingredient_in_fridge.quantity:
        ingredient_in_fridge.allocated_quantity = ingredient_in_fridge.quantity


class Recipe(BaseModel):
    id: int = None
    ingredients: List[Ingredient]


class ShoppingList(BaseModel):
    items: Dict[str, float]


@attr.s
class ShoppingListLogic:
    _ingredients_in_fridge: List[ProductInFridge] = attr.ib()
    shopping_list: ShoppingList = None

    def create(self, recipes: List[Recipe]):
        self.shopping_list = ShoppingList(items={})
        for recipe in recipes:
            for ingredient_in_recipe in recipe.ingredients:
                quantity_available_in_fridge = 0
                try:
                    ingredient_in_fridge = next(
                        filter(lambda in_fridge: in_fridge.name == ingredient_in_recipe.name,
                               self._ingredients_in_fridge))
                    quantity_available_in_fridge = ingredient_in_fridge.quantity -\
                                                   ingredient_in_fridge.allocated_quantity
                    set_allocated_quantity(ingredient_in_fridge, ingredient_in_recipe)
                except StopIteration:
                    pass
                # neglect possible mismatch of units for now
                if quantity_available_in_fridge < ingredient_in_recipe.quantity:
                    self._add(ingredient_in_recipe, quantity_available_in_fridge)
    
    def _add(self, ingredient_in_recipe: Ingredient, quantity_available_in_fridge: float = 0.0):
        quantity_to_buy = ingredient_in_recipe.quantity - quantity_available_in_fridge
        if ingredient_in_recipe.name in self.shopping_list.items:
            self.shopping_list.items[ingredient_in_recipe.name] += quantity_to_buy
        else:
            self.shopping_list.items[ingredient_in_recipe.name] = quantity_to_buy


class Fridge(BaseModel):
    owner: int
    products: List[ProductInFridge]


@attr.s
class FridgeLogic:
    fridge: Fridge

    def add_product(self, product: ProductInFridge):
        pass

    def remove_product(self, product: ProductInFridge):
        pass
