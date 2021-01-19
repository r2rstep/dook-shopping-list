from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from shopping_list import domain
from shopping_list.api import resp_models
from ..helpers.data_generators import random_recipe, random_fridge_to_db


@pytest.mark.end2end
def test_create_shopping_list(db: Session, client: TestClient):
    recipe = random_recipe(db)
    fridge = random_fridge_to_db(db)
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
    fridge = random_fridge_to_db(db)
    shopping_list = client.post(f'/fridges/{fridge.id}/shoppingLists',
                                json=domain.commands.CreateShoppingList(recipes=[recipe.id]).dict())
    assert shopping_list.status_code == 201
    created_shopping_list = resp_models.ShoppingList(**shopping_list.json())

    resp = client.get(created_shopping_list.links.self)
    retrieved_shopping_list = resp_models.ShoppingList(**resp.json())
    assert retrieved_shopping_list.shopping_list == created_shopping_list.shopping_list


@pytest.mark.end2end
def test_change_fridge_contents_should_update_shopping_list(db: Session, client: TestClient):
    recipe = random_recipe(db)
    fridge = random_fridge_to_db(db)
    shopping_list = client.post(f'/fridges/{fridge.id}/shoppingLists',
                                json=domain.commands.CreateShoppingList(recipes=[recipe.id]).dict())
    assert shopping_list.status_code == 201
    shopping_list_v1 = resp_models.ShoppingList(**shopping_list.json())
    assert shopping_list_v1.shopping_list.items

    # add products from the shopping list so that the updated shopping list becomes empty
    products_changes = list(map(lambda p: domain.fridge.ProductUpdate(name=p[0],
                                                                      quantity=p[1]),
                                shopping_list_v1.shopping_list.items.items()))
    shopping_list = client.patch(f'/fridges/{fridge.id}/products',
                                 json=domain.commands.ChangeFridgeContents(products=products_changes).dict())
    assert shopping_list.status_code == 200

    # temporarily assume that the client will poll for shopping list updates
    updated_shopping_list = client.get(shopping_list_v1.links.self)
    shopping_list_v2 = resp_models.ShoppingList(**updated_shopping_list.json()).shopping_list.items
    assert not shopping_list_v2, f'Shopping list not empty for {shopping_list_v1.links.self}'
