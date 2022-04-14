import uuid
from .. import db


class CartItem(db.Model):
    __tablename__ = "cart_item"

    cart_item_id = db.Column(db.String(255), primary_key=True, default=lambda: uuid.uuid4())
    product_id = db.Column(db.String(255), default=lambda: uuid.uuid4())
    quantity = db.Column(db.Integer, nullable=False)
    subtotal_ex_tax = db.Column(db.Float)
    tax_total = db.Column(db.Float)
    total = db.Column(db.Float)
    cart_id = db.Column(db.String(255), db.ForeignKey('cart.cart_id'), default=lambda: uuid.uuid4())
