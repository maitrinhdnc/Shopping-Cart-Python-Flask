import uuid
from .. import db


class Product(db.Model):
    __tablename__ = "product"

    product_id = db.Column(db.String(255), primary_key=True, default=lambda: uuid.uuid4())
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
