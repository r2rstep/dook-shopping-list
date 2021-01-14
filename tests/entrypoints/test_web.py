from shopping_list.adapters import db

from ..helpers.recipes import random_recipe


def test_create_shopping_list():
    recipe = random_recipe(db.session.session())
    pass
