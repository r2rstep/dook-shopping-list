from typing import List

from sqlalchemy.orm import Session

from ..domain import models, commands
from ..adapters.db import repo_sqlalchemy as repos, models as db_models


def create_shopping_list(db: Session,
                         command: commands.CreateShoppingList,
                         fridge_id: int) -> models.ShoppingList:
    fridge_db: db_models.Fridge
    fridge: models.Fridge
    fridge_db, fridge = repos.fridge.get(db, id=fridge_id)
    recipes: List[models.Recipe] = []
    for recipe_id in command.recipes:
        recipes.append(repos.recipe.get(db, id=recipe_id)[1])
    logic = models.ShoppingListLogic(fridge=models.FridgeLogic(fridge=fridge))
    logic.create(recipes)
    repos.shopping_list.add(db, obj_in=logic.shopping_list)
    repos.fridge.update(db, db_obj=fridge_db, obj_in=fridge)
    return logic.shopping_list
