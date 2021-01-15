from pydantic import BaseModel

from .. import domain


class ShoppingList(BaseModel):
    class Links(BaseModel):
        self: str = ''
        fridge: str = ''

    shopping_list: domain.models.ShoppingList
    links: Links = Links()
