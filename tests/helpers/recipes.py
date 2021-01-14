import random

from sqlalchemy.orm import Session

from shopping_list.adapters.db import repo_sqlalchemy as repos
from shopping_list.domain import models
from .utils import random_lower_string


def random_recipe(session: Session) -> models.Recipe:
    recipe = models.Recipe(ingredients=[])
    recipe_repo = repos.Recipe(session)
    for idx in range(0, random.randint(3, 10)):
        recipe.ingredients.append(models.Ingredient(name=random_lower_string(),
                                                    quantity=random.randint(1, 10),
                                                    unit=models.QuantityUnits.units))
    return recipe_repo.add(recipe)
