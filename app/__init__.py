from flask_restx import Api
from flask import Blueprint

from .main.controller.auth_controller import api as auth_ns
from .main.controller.cart_item_controller import api as cart_item_ns
from .main.controller.cart_controller import api_cart as cart_ns
from .main.controller.user_controller import api as user_ns
from .main.controller.product_controller import api as product_ns


blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='Exercise 1 - SHOP ONLINE',
    version='1.0',
    description='',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(auth_ns)
api.add_namespace(cart_item_ns, path='/cart-item')
api.add_namespace(cart_ns, path='/cart')
api.add_namespace(user_ns, path='/user')
api.add_namespace(product_ns, path='/product')

