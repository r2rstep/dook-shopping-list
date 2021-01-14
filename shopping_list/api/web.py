from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask('shopping_list')


@app.route('/shoppingList', methods=['POST'])
def create_shopping_list():
    pass
