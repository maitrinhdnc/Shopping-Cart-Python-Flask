from flask_restx import Namespace, fields

class UserDto:
    api = Namespace('user', description = 'user related operations')
    user = api.model('user', {
        'email': fields.String(required = True, description = 'user email address'),
        'username': fields.String(required = True, description = 'user username'),
        'password': fields.String(required = True, description = 'user password'),
    })

class AuthDto:
    api = Namespace('auth', description = 'authentication related operations')
    user_auth = api.model('auth', {
        'email': fields.String(required = True, description = 'The email address'),
        'password': fields.String(required = True, description = 'The user password '),
    })

class CartItemDto:
    api = Namespace('cart_item', description = 'cart item related operations')
    cart_item = api.model('cart_item', {
        'quantity': fields.Integer(required = True, description = 'cart item quantity'),
    })

class CartDto:
    api = Namespace('cart', description = 'cart related operations')
    cart = api.model('cart', {
        'product_id': fields.String(required = True, description = 'productid'),
        'quantity': fields.Integer(required = True, description = 'cart quantity'),
    })

class ProductDto:
    api = Namespace('product', description = 'product related operations')
    product = api.model('product', {
        'name': fields.String(required = True, description = 'product name'),
        'price': fields.Float(required = True, description = 'product price'),

    })

