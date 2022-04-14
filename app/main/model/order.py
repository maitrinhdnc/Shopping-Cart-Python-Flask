import uuid
from .. import db


class Order(db.Model):
    __tablename__ = "order"

    order_id = db.Column(db.String(255), primary_key=True, default=uuid.uuid4())
    user_id = db.Column(db.String(255), nullable=False)
    order_items = db.relationship('OrderItem', backref='order')
    subtotal_ex_tax = db.Column(db.Float)
    tax_total = db.Column(db.Float)
    total = db.Column(db.Float)
    payment_status = db.Column(db.String(20), nullable=False)

