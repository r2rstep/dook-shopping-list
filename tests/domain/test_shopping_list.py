from shopping_list.domain import models


def test_create_shopping_list_for_single_recipe__some_ingredients_missing():
    ingredients_in_fridge = [
        models.IngredientInFridge(name='banana', quantity=4, unit=models.QuantityUnits.units),
        models.IngredientInFridge(name='avocado', quantity=1, unit=models.QuantityUnits.units),
        models.IngredientInFridge(name='salad', quantity=1, unit=models.QuantityUnits.units)]

    recipe = models.Recipe(
        ingredients=[models.Ingredient(name='salad', quantity=1, unit=models.QuantityUnits.units),
                     models.Ingredient(name='pear', quantity=1, unit=models.QuantityUnits.units),
                     models.Ingredient(name='almond', quantity=40, unit=models.QuantityUnits.gram),
                     models.Ingredient(name='goat cheese', quantity=80,
                                       unit=models.QuantityUnits.gram)])

    shopping_list = models.ShoppingList(ingredients_in_fridge=ingredients_in_fridge)
    shopping_list.create([recipe])

    assert shopping_list.items == {'pear': 1,
                                   'almond': 40,
                                   'goat cheese': 80}
    assert ingredients_in_fridge[2].allocated_quantity == 1.0
