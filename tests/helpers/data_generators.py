import random

from sqlalchemy.orm import Session

from shopping_list.adapters.db import repo_sqlalchemy as repos
from shopping_list.domain import models
from .utils import random_lower_string


def random_recipe(session: Session) -> models.Recipe:
    recipe = models.Recipe(ingredients=[])
    for idx in range(0, random.randint(3, 10)):
        recipe.ingredients.append(models.Ingredient(name=random_lower_string(),
                                                    quantity=random.randint(1, 10),
                                                    unit=models.QuantityUnits.units))
    return repos.recipe.add(session, obj_in=recipe)


def random_fridge(session: Session) -> models.Fridge:
    fridge = models.Fridge(owner=random.randint(0, 100), products=[])
    for idx in range(0, random.randint(3, 10)):
        fridge.products.append(models.ProductInFridge(name=random_lower_string(),
                                                      quantity=random.randint(1, 10),
                                                      unit=models.QuantityUnits.units))
    return repos.fridge.add(session, obj_in=fridge)
