from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from shopping_list import domain
from shopping_list.api import resp_models
from ..helpers.data_generators import random_recipe, random_fridge


@pytest.mark.end2end
def test_create_shopping_list(db: Session, client: TestClient):
    recipe = random_recipe(db)
    fridge = random_fridge(db)
    shopping_list = client.post(f'/fridges/{fridge.id}/shoppingLists',
                                json=domain.commands.CreateShoppingList(recipes=[recipe.id]).dict())
    assert shopping_list.status_code == 201

    expected_list = {ingredient.name: ingredient.quantity for ingredient in recipe.ingredients}
    resp_data = resp_models.ShoppingList(**shopping_list.json())
    assert resp_data.shopping_list.items == expected_list
    assert resp_data.links.fridge == f'/fridges/{fridge.id}'
    assert f'/fridges/{fridge.id}/shoppingLists' in resp_data.links.self


@pytest.mark.end2end
def test_get_shopping_list(db: Session, client: TestClient):
    recipe = random_recipe(db)
    fridge = random_fridge(db)
    shopping_list = client.post(f'/fridges/{fridge.id}/shoppingLists',
                                json=domain.commands.CreateShoppingList(recipes=[recipe.id]).dict())
    assert shopping_list.status_code == 201
    created_shopping_list = resp_models.ShoppingList(**shopping_list.json())

    resp = client.get(created_shopping_list.links.self)
    retrieved_shopping_list = resp_models.ShoppingList(**resp.json())
    assert retrieved_shopping_list.shopping_list == created_shopping_list.shopping_list
