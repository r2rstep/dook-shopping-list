from typing import List

import attr
from pydantic import BaseModel

from .event import Event


class ProductBase(BaseModel):
    name: str
    quantity: float


class ProductUpdate(ProductBase):
    pass


class ProductInFridge(ProductBase):
    allocated_quantity: float = 0.0

    class Config:
        orm_mode = True


class Fridge(BaseModel):
    id: int = None
    owner: int
    products: List[ProductInFridge]

    class Config:
        orm_mode = True


class FridgeContentChanged(Event):
    fridge_id: int
    changed_products: List[ProductUpdate]


@attr.s(auto_attribs=True)
class FridgeLogic:
    fridge: Fridge
    events: List[Event] = attr.ib(factory=list)

    def allocate_product(self, ingredient: ProductBase) -> float:
        try:
            ingredient_in_fridge = next(filter(lambda product: product.name == ingredient.name,
                                               self.fridge.products))
        except StopIteration:
            return 0
        ingredient_in_fridge.allocated_quantity += ingredient.quantity
        this_allocation_quantity = ingredient.quantity
        if ingredient_in_fridge.allocated_quantity > ingredient_in_fridge.quantity:
            this_allocation_quantity = ingredient.quantity - (ingredient_in_fridge.allocated_quantity -
                                                              ingredient_in_fridge.quantity)
            ingredient_in_fridge.allocated_quantity = ingredient_in_fridge.quantity
        return this_allocation_quantity

    def update_contents(self, products: List[ProductUpdate]):
        current_products = {p.name: p for p in self.fridge.products}
        event = FridgeContentChanged(fridge_id=self.fridge.id, changed_products=[])
        for changed_product in products:
            self._add_changed_product_to_event(changed_product, current_products, event)
            allocated_quantity = current_products.get(
                changed_product.name,
                ProductInFridge(**changed_product.dict())).allocated_quantity
            current_products.update({changed_product.name: ProductInFridge(
                **changed_product.dict(),
                allocated_quantity=allocated_quantity)})
            if not current_products[changed_product.name].quantity:
                del current_products[changed_product.name]
        self.fridge.products = list(current_products.values())
        self.events.append(event)

    def _add_changed_product_to_event(self, changed_product, current_products, event):
        event.changed_products.append(ProductUpdate(**changed_product.dict()))
        if changed_product.name in current_products:
            event.changed_products[-1].quantity = changed_product.quantity - \
                                                  current_products[changed_product.name].quantity
