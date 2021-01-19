from shopping_list.domain.fridge import ProductInFridge, FridgeLogic, Ingredient, Fridge
from shopping_list.domain.shopping_list import ShoppingListLogic, ShoppingList, Recipe


def test_create_shopping_list():
    avocado_in_fridge = ProductInFridge(name='avocado', quantity=1)
    salad_in_fridge = ProductInFridge(name='salad', quantity=1)
    banana_in_fridge = ProductInFridge(name='banana', quantity=4)
    goat_cheese_in_fridge = ProductInFridge(name='goat cheese', quantity=100)
    products_in_fridge = [
        banana_in_fridge,
        avocado_in_fridge,
        salad_in_fridge,
        goat_cheese_in_fridge]
    fridge = Fridge(products=products_in_fridge, owner=0)

    shopping_list = ShoppingListLogic(FridgeLogic(fridge))
    shopping_list.create([
        Recipe(
            name='salad',
            ingredients=[Ingredient(name='salad', quantity=1),
                         Ingredient(name='pear', quantity=1),
                         Ingredient(name='almond', quantity=40),
                         Ingredient(name='goat cheese', quantity=80)]),
        Recipe(
            name='salad',
            ingredients=[Ingredient(name='avocado', quantity=3),
                         Ingredient(name='almond', quantity=20),
                         Ingredient(name='salad', quantity=1)]
        )
    ])

    assert shopping_list.shopping_list.items == {'pear': 1,
                                                 'almond': 60,
                                                 'salad': 1,
                                                 'avocado': 2}
    assert next(filter(lambda p: p.name == 'avocado', fridge.products)).allocated_quantity == 1.0
    assert next(filter(lambda p: p.name == 'salad', fridge.products)).allocated_quantity == 1.0
    assert next(filter(lambda p: p.name == 'goat cheese', fridge.products)).allocated_quantity == 80.0


def test_removing_fridge_contents_should_increase_quantity_on_shopping_list_and_update_allocation():
    shopping_list = ShoppingList(items=dict(pear=1, almond=60, salad=1, avocado=2))

    fridge = Fridge(products=[ProductInFridge(name='avocado', quantity=1, allocated_quantity=2)],
                    owner=0)
    expected_fridge = Fridge(products=[ProductInFridge(name='avocado', quantity=1, allocated_quantity=1)],
                             owner=0)
    logic = ShoppingListLogic(shopping_list=shopping_list, fridge=FridgeLogic(fridge))
    logic.update([ProductInFridge(name='pear', quantity=-1), ProductInFridge(name='avocado', quantity=-1)])

    assert logic.shopping_list.items == dict(pear=2, almond=60, salad=1, avocado=3)
    assert fridge == expected_fridge


def test_adding_fridge_contents_should_decrease_quantity_on_shopping_list_and_update_allocation():
    shopping_list = ShoppingList(items=dict(pear=1, almond=60, salad=1, avocado=2))

    fridge = Fridge(products=[ProductInFridge(name='pear', quantity=2, allocated_quantity=0),
                              ProductInFridge(name='avocado', quantity=1, allocated_quantity=0)],
                    owner=0)
    expected_fridge = Fridge(products=[ProductInFridge(name='pear', quantity=2, allocated_quantity=2),
                                       ProductInFridge(name='avocado', quantity=1, allocated_quantity=1)],
                             owner=0)
    logic = ShoppingListLogic(shopping_list=shopping_list, fridge=FridgeLogic(fridge))
    logic.update([ProductInFridge(name='pear', quantity=2),
                  ProductInFridge(name='watermelon', quantity=1),
                  ProductInFridge(name='avocado', quantity=1)])

    assert logic.shopping_list.items == dict(almond=60, salad=1, avocado=1)
    assert fridge == expected_fridge
