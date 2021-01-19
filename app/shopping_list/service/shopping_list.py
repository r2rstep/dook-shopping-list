from typing import List

from sqlalchemy.orm import Session

from ..domain import shopping_list as shopping_list_models, fridge as fridge_models, commands
from ..adapters.db import repo_sqlalchemy as repos, models as db_models


def create_shopping_list(db: Session,
                         command: commands.CreateShoppingList,
                         fridge_id: int) -> shopping_list_models.ShoppingList:
    fridge_db: db_models.Fridge
    fridge: fridge_models.Fridge
    fridge_db, fridge = repos.fridge.get(db, id=fridge_id)
    recipes: List[shopping_list_models.Recipe] = []
    for recipe_id in command.recipes:
        recipes.append(repos.recipe.get(db, id=recipe_id)[1])
    logic = shopping_list_models.ShoppingListLogic(fridge=fridge_models.FridgeLogic(fridge=fridge))
    logic.create(recipes)
    repos.fridge.update(db, db_obj=fridge_db, obj_in=fridge)
    return repos.shopping_list.add(db, obj_in=logic.shopping_list)[1]


def update_shopping_lists(db: Session, event: fridge_models.FridgeContentChanged):
    fridge_db: db_models.Fridge
    fridge: fridge_models.Fridge
    fridge_db, fridge = repos.fridge.get(db, id=event.fridge_id)
    for shopping_list_db in fridge_db.shopping_lists:
        logic = shopping_list_models.ShoppingListLogic(
            fridge=fridge_models.FridgeLogic(fridge=fridge),
            shopping_list=shopping_list_models.ShoppingList.from_orm(shopping_list_db))
        logic.update(event.changed_products)
        repos.fridge.update(db, db_obj=fridge_db, obj_in=fridge)
        repos.shopping_list.update(db, db_obj=shopping_list_db, obj_in=logic.shopping_list)
