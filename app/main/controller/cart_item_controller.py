from flask import request
from flask_restx import Resource

from ..util.dto import CartItemDto
from ..service.cart_service import change_quantity_cart_item, delete_cart_item

api = CartItemDto.api
cart_item = CartItemDto.cart_item

@api.route('/<cart_item_id>/changeqty')
class CartItem(Resource):
    @api.expect(cart_item, validate=True)
    @api.response(201, 'Cart successfully created.')
    @api.doc('change quality cart item')
    def put(self, cart_item_id):
        """Change quality cart item"""
        data = request.json
        return change_quantity_cart_item(cart_item_id, data=data)

@api.route('/<cart_item_id>')
@api.param('cart_item_id', 'The cart item id using to get cart item')
class CartItem(Resource):
    @api.response(200, 'delete cart item successfully.')
    @api.doc('delete cart item cart item')
    def delete(self,cart_item_id):
        """Delete Cart Item"""
        return delete_cart_item(cart_item_id)