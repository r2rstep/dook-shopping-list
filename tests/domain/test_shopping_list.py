from shopping_list.domain import models


def test_create_shopping_list():
    avocado_in_fridge = models.ProductInFridge(name='avocado', quantity=1, unit=models.QuantityUnits.units)
    salad_in_fridge = models.ProductInFridge(name='salad', quantity=1, unit=models.QuantityUnits.units)
    banana_in_fridge = models.ProductInFridge(name='banana', quantity=4, unit=models.QuantityUnits.units)
    goat_cheese_in_fridge = models.ProductInFridge(name='goat cheese', quantity=100,
                                                   unit=models.QuantityUnits.gram)
    ingredients_in_fridge = [
        banana_in_fridge,
        avocado_in_fridge,
        salad_in_fridge,
        goat_cheese_in_fridge]

    shopping_list = models.ShoppingList(ingredients_in_fridge=ingredients_in_fridge)
    shopping_list.create([
        models.Recipe(
            ingredients=[models.Ingredient(name='salad', quantity=1, unit=models.QuantityUnits.units),
                         models.Ingredient(name='pear', quantity=1, unit=models.QuantityUnits.units),
                         models.Ingredient(name='almond', quantity=40, unit=models.QuantityUnits.gram),
                         models.Ingredient(name='goat cheese', quantity=80,
                                           unit=models.QuantityUnits.gram)]),
        models.Recipe(
            ingredients=[models.Ingredient(name='avocado', quantity=3, unit=models.QuantityUnits.units),
                         models.Ingredient(name='almond', quantity=20, unit=models.QuantityUnits.gram),
                         models.Ingredient(name='salad', quantity=1, unit=models.QuantityUnits.units)]
        )
    ])

    assert shopping_list.items == {'pear': 1,
                                   'almond': 60,
                                   'salad': 1,
                                   'avocado': 2}
    assert avocado_in_fridge.allocated_quantity == 1.0
    assert salad_in_fridge.allocated_quantity == 1.0
    assert goat_cheese_in_fridge.allocated_quantity == 80.0
