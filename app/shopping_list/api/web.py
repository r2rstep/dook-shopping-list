from fastapi import FastAPI, status, Depends
from starlette.requests import Request

from . import resp_models, deps
from .. import domain
from ..service.shopping_list import create_shopping_list as srv_create_shopping_list


app = FastAPI()


@app.post('/fridges/{fridge_id}/shoppingList',
          response_model=resp_models.ShoppingList,
          status_code=status.HTTP_201_CREATED)
def create_shopping_list(command: domain.commands.CreateShoppingList,
                         fridge_id: int,
                         req: Request,
                         db=Depends(deps.get_db)):
    shopping_list = srv_create_shopping_list(db, command, fridge_id)
    resp = resp_models.ShoppingList(shopping_list=shopping_list)
    resp.links.self = req.url.path
    resp.links.fridge = req.url.path.rstrip('/shoppingList')
    return resp
