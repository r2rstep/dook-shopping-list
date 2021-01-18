import copy
from typing import List

import pytest

from shopping_list.domain import models


def test_create_shopping_list():
    avocado_in_fridge = models.ProductInFridge(name='avocado', quantity=1)
    salad_in_fridge = models.ProductInFridge(name='salad', quantity=1)
    banana_in_fridge = models.ProductInFridge(name='banana', quantity=4)
    goat_cheese_in_fridge = models.ProductInFridge(name='goat cheese', quantity=100)
    products_in_fridge = [
        banana_in_fridge,
        avocado_in_fridge,
        salad_in_fridge,
        goat_cheese_in_fridge]
    fridge = models.Fridge(products=products_in_fridge, owner=0)

    shopping_list = models.ShoppingListLogic(models.FridgeLogic(fridge))
    shopping_list.create([
        models.Recipe(
            ingredients=[models.Ingredient(name='salad', quantity=1),
                         models.Ingredient(name='pear', quantity=1),
                         models.Ingredient(name='almond', quantity=40),
                         models.Ingredient(name='goat cheese', quantity=80)]),
        models.Recipe(
            ingredients=[models.Ingredient(name='avocado', quantity=3),
                         models.Ingredient(name='almond', quantity=20),
                         models.Ingredient(name='salad', quantity=1)]
        )
    ])

    assert shopping_list.shopping_list.items == {'pear': 1,
                                                 'almond': 60,
                                                 'salad': 1,
                                                 'avocado': 2}
    assert next(filter(lambda p: p.name == 'avocado', fridge.products)).allocated_quantity == 1.0
    assert next(filter(lambda p: p.name == 'salad', fridge.products)).allocated_quantity == 1.0
    assert next(filter(lambda p: p.name == 'goat cheese', fridge.products)).allocated_quantity == 80.0


@pytest.mark.parametrize('changed_products,expected_list',
                         [([models.ProductInFridge(name='pear', quantity=2),
                            models.ProductInFridge(name='watermelon', quantity=1),
                            models.ProductInFridge(name='avocado', quantity=1)],
                           dict(almond=60, salad=1, avocado=1)),
                          ([models.ProductInFridge(name='pear', quantity=-1),
                            models.ProductInFridge(name='watermelon', quantity=1),
                            models.ProductInFridge(name='avocado', quantity=-1)],
                           dict(pear=2, almond=60, salad=1, avocado=3))])
def test_changing_fridge_contents_should_change_its_quantity_on_shopping_list(
        changed_products: List[models.ProductInFridge],
        expected_list: dict
):
    shopping_list = models.ShoppingList(items=dict(pear=1, almond=60, salad=1, avocado=2))

    logic = models.ShoppingListLogic(shopping_list=shopping_list)
    logic.update(changed_products)

    assert logic.shopping_list.items == expected_list
