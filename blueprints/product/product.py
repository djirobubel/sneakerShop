from flask import Blueprint
from models import *

product_bp = Blueprint('product', __name__)


@product_bp.route('/products')
def get_products():
    products = Product.select().limit(10).order_by(Product.id.desc())
    output = []

    for product in products:
        product_data = {'id': product.id, 'model': product.model, 'price': product.price}
        output.append(product_data)

    return output


@product_bp.route('/products/<id>')
def get_product(id):
    try:
        product = Product.get(Product.id == id)

        queries = ProductSize.select().where(ProductSize.product_id == id)
        output = []
        for query in queries:
            sizes = Size.select().where(Size.id == query.size_id)
            for size in sizes:
                size_data = size.us_size
                output.append(size_data)

        return {'model': product.model, 'description': product.description, 'sizes': output, 'price': product.price}

    except Product.DoesNotExist:
        return {'error': 'product not found'}, 404

