import random
from typing import Type

from sqlalchemy.orm import Session

from shopping_list.adapters.db import repo_sqlalchemy as repos
from shopping_list.domain import fridge as fridge_models
from shopping_list.domain import shopping_list as shopping_list_models
from .utils import random_lower_string


def random_recipe(session: Session) -> shopping_list_models.Recipe:
    recipe = shopping_list_models.Recipe(ingredients=[])
    for idx in range(0, random.randint(3, 10)):
        recipe.ingredients.append(random_product(shopping_list_models.Ingredient))
    return repos.recipe.add(session, obj_in=recipe)[1]


def random_fridge_to_db(session: Session) -> fridge_models.Fridge:
    fridge = random_fridge()
    fridge.id = None
    return repos.fridge.add(session, obj_in=fridge)[1]


def random_fridge() -> fridge_models.Fridge:
    fridge = fridge_models.Fridge(id=random.randint(0, 100), owner=random.randint(0, 100), products=[])
    for idx in range(0, random.randint(3, 10)):
        fridge.products.append(random_product(fridge_models.ProductInFridge))
    return fridge


def random_product(klass: Type):
    return klass(name=random_lower_string(), quantity=random.randint(1, 10))
