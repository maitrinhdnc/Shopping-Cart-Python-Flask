import uuid
from .. import db


class Cart(db.Model):
    __tablename__ = "cart"

    cart_id = db.Column(db.String(255), primary_key=True, default=uuid.uuid4())
    userId = db.Column(db.String(255), unique=True, nullable=False)
    cart_items = db.relationship('CartItem', backref='cart', cascade="all, delete-orphan")
    subtotal_ex_tax = db.Column(db.Float)
    tax_total = db.Column(db.Float)
    total = db.Column(db.Float)

