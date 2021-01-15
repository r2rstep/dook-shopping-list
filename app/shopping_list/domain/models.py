from typing import List, Dict

import attr
from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    quantity: float

    class Config:
        orm_mode = True


class ProductInFridge(Ingredient):
    allocated_quantity: float = 0.0

    class Config:
        orm_mode = True


class Recipe(BaseModel):
    id: int = None
    ingredients: List[Ingredient]

    class Config:
        orm_mode = True


class ShoppingList(BaseModel):
    items: Dict[str, float]

    class Config:
        orm_mode = True


class Fridge(BaseModel):
    id: int = None
    owner: int
    products: List[ProductInFridge]

    class Config:
        orm_mode = True


@attr.s(auto_attribs=True)
class FridgeLogic:
    fridge: Fridge

    def allocate_product(self, ingredient: Ingredient):
        ingredient_in_fridge = next(filter(lambda product: product.name == ingredient.name,
                                           self.fridge.products))
        ingredient_in_fridge.allocated_quantity += ingredient.quantity
        this_allocation_quantity = ingredient.quantity
        if ingredient_in_fridge.allocated_quantity > ingredient_in_fridge.quantity:
            this_allocation_quantity = ingredient.quantity - (ingredient_in_fridge.allocated_quantity -
                                                              ingredient_in_fridge.quantity)
            ingredient_in_fridge.allocated_quantity = ingredient_in_fridge.quantity
        return this_allocation_quantity


@attr.s(auto_attribs=True)
class ShoppingListLogic:
    _fridge: FridgeLogic
    shopping_list: ShoppingList = None

    def create(self, recipes: List[Recipe]):
        self.shopping_list = ShoppingList(items={})
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
    
    def _add(self, ingredient_in_recipe: Ingredient, quantity_available_in_fridge: float = 0.0):
        quantity_to_buy = ingredient_in_recipe.quantity - quantity_available_in_fridge
        if ingredient_in_recipe.name in self.shopping_list.items:
            self.shopping_list.items[ingredient_in_recipe.name] += quantity_to_buy
        else:
            self.shopping_list.items[ingredient_in_recipe.name] = quantity_to_buy
