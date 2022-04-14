import uuid
from .. import db


class OrderItem(db.Model):
    __tablename__ = "order_item"

    order_item_id = db.Column(db.String(255), primary_key=True)
    product_id = db.Column(db.String(255), default=lambda: uuid.uuid4())
    quantity = db.Column(db.Integer, nullable=False)
    subtotal_ex_tax = db.Column(db.Float)
    tax_total = db.Column(db.Float)
    total = db.Column(db.Float)
    order_id = db.Column(db.String(255), db.ForeignKey('order.order_id'), default=lambda: uuid.uuid4())
 