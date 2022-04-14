from flask import request
from flask_restx import Resource

from ..util.dto import ProductDto
from ..service.product_service import add_product

api = ProductDto.api
product = ProductDto.product

@api.route('/add')
class ProductAdd(Resource):
    @api.expect(product, validate=True)
    @api.response(201, 'Product successfully created.')
    def put(self):
        """Create a new product """
        data = request.json
        return add_product(data=data)
