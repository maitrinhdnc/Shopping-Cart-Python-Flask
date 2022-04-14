from app.main.model.product import Product
from typing import Dict
from app.main import db

def add_product(data: Dict[str, str]):
    product = Product.query.filter_by(name= data['name']).first()
    if not product:
        new_cart = Product(
                name = data['name'],
                price = data['price']
            )
        save_changes(new_cart)
    return "Add product succesfully", 200
    
def save_changes(data: Product):
    db.session.add(data)
    db.session.commit()