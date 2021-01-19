import copy

from shopping_list.domain import fridge as fridge_models
from ..helpers.data_generators import random_fridge, random_product


class TestProductsAllocation:
    def test_full_allocation(self):
        fridge = random_fridge()
        logic = fridge_models.FridgeLogic(fridge)

        fully_allocated_product = copy.deepcopy(fridge.products[0])
        assert logic.allocate_product(fridge_models.Ingredient(**fully_allocated_product.dict())) == \
               fully_allocated_product.quantity
        assert fridge.products[0].allocated_quantity == fully_allocated_product.quantity

    def test_partial_allocation(self):
        fridge = random_fridge()
        logic = fridge_models.FridgeLogic(fridge)

        partially_allocated_product = copy.deepcopy(fridge.products[0])
        partially_allocated_product.quantity *= 0.5
        allocation_req = fridge_models.Ingredient(**partially_allocated_product.dict())
        assert logic.allocate_product(allocation_req) == partially_allocated_product.quantity
        assert fridge.products[0].allocated_quantity == partially_allocated_product.quantity

    def test_over_allocation(self):
        fridge = random_fridge()
        logic = fridge_models.FridgeLogic(fridge)

        over_allocation_req = copy.deepcopy(fridge.products[0])
        over_allocation_req.quantity *= 1.5
        allocation_req = fridge_models.Ingredient(**over_allocation_req.dict())
        assert logic.allocate_product(allocation_req) == fridge.products[0].quantity
        assert fridge.products[0].allocated_quantity == fridge.products[0].quantity


def test_contents_update():
    fridge = random_fridge()

    changed_products = copy.deepcopy(fridge.products[0:2])
    changed_products[0].quantity *= 0.5
    changed_products[1].quantity = 0
    new_product = random_product(fridge_models.ProductInFridge)
    products_diff = [fridge_models.ProductInFridge(
        name=changed.name,
        quantity=changed.quantity - current.quantity) for changed, current in zip(changed_products,
                                                                                  fridge.products)]
    products_diff.append(new_product)
    expected_products = [changed_products[0]] + copy.deepcopy(fridge.products[2:]) + [new_product]

    logic = fridge_models.FridgeLogic(fridge)
    logic.update_contents(changed_products + [new_product])

    assert logic.fridge.products == expected_products

    expected_event = fridge_models.FridgeContentChanged(fridge_id=fridge.id, changed_products=products_diff)
    assert logic.events == [expected_event]
