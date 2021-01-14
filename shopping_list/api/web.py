from fastapi import FastAPI, status
from starlette.requests import Request

from .. import domain
from . import resp_models


app = FastAPI()


@app.post('/fridges/{fridge_id}/shoppingList',
          response_model=resp_models.ShoppingList,
          status_code=status.HTTP_201_CREATED)
def create_shopping_list(command: domain.commands.CreateShoppingList,
                         fridge_id: int,
                         req: Request):
    shopping_list = resp_models.ShoppingList(shopping_list=domain.models.ShoppingList(items={}))
    shopping_list.links.self = req.url.path
    shopping_list.links.fridge = req.url.path.rstrip('/shoppingList')
    return shopping_list
