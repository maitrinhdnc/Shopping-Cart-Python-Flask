from flask import request
from flask_restx import Resource

from ..util.dto import CartDto
from ..service.cart_service import add_cart, checkout_cart
from ..service.order_service import update_order_status

api_cart = CartDto.api
cart = CartDto.cart

@api_cart.route('/add')
class CartAdd(Resource):
    @api_cart.expect(cart, validate=True)
    def post(self):
        """Creates A New Cart"""
        data = request.json
        return add_cart(data=data)

@api_cart.route('/checkout')
class CartCheckOut(Resource):
    def post(self):
        """Checkout Cart"""
        return checkout_cart()

@api_cart.route('/update-order-status')
class OrderStatus(Resource):
    def post(self):
        data = request.json
        return update_order_status(data.get("tags"))