from typing import List, Dict

import attr
from pydantic import BaseModel

from .fridge import Ingredient, ProductInFridge, FridgeLogic


class Recipe(BaseModel):
    id: int = None
    name: str
    ingredients: List[Ingredient]

    class Config:
        orm_mode = True


class ShoppingList(BaseModel):
    id: int = None
    items: Dict[str, float]
    fridge_id: int = None

    class Config:
        orm_mode = True


@attr.s(auto_attribs=True)
class ShoppingListLogic:
    _fridge: FridgeLogic = None
    shopping_list: ShoppingList = None

    def create(self, recipes: List[Recipe]):
        self.shopping_list = ShoppingList(items={}, fridge_id=self._fridge.fridge.id)
        for recipe in recipes:
            for ingredient_in_recipe in recipe.ingredients:
                quantity_available_in_fridge = 0
                try:
                    quantity_available_in_fridge = self._fridge.allocate_product(ingredient_in_recipe)
                except StopIteration:
                    pass
                # neglect possible mismatch of units for now
                if quantity_available_in_fridge < ingredient_in_recipe.quantity:
                    self._add(ingredient_in_recipe, quantity_available_in_fridge)

    def update(self, products_changes: List[ProductInFridge]):
        for changed_product in products_changes:
            if changed_product.name in self.shopping_list.items:
                self.shopping_list.items[changed_product.name] -= changed_product.quantity
                if self.shopping_list.items[changed_product.name] <= 0:
                    del self.shopping_list.items[changed_product.name]
    
    def _add(self, ingredient_in_recipe: Ingredient, quantity_available_in_fridge: float = 0.0):
        quantity_to_buy = ingredient_in_recipe.quantity - quantity_available_in_fridge
        if ingredient_in_recipe.name in self.shopping_list.items:
            self.shopping_list.items[ingredient_in_recipe.name] += quantity_to_buy
        else:
            self.shopping_list.items[ingredient_in_recipe.name] = quantity_to_buy
