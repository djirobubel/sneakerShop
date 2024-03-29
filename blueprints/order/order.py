from flask import Blueprint, request, Response
from models import *

order_bp = Blueprint('order', __name__)


@order_bp.route('/orders/<id>')
def get_order(id):
    try:
        order = Order.get(Order.id == id)

        order_items = OrderItem.select().where(OrderItem.order_id == order.id)

        output = []
        for order_item in order_items:
            product_model = Product.get(Product.id == order_item.product_id)
            product_size = Size.get(Size.id == order_item.size_id)
            order_item_data = {'model': product_model.model, 'size': product_size.us_size,
                               'quantity': order_item.quantity,
                               'price': order_item.price}
            output.append(order_item_data)

        return {'items': output}

    except Order.DoesNotExist:
        return {'error': 'order not found'}, 404


@order_bp.route('/orders', methods=['POST'])
def create_order():
    with db.atomic() as transaction:
        try:
            order = Order.create(customer_id=request.json['customerId'])
            Customer.get(Customer.id == order.customer_id)

            items = request.json['items']
            for item in items:
                try:
                    new_product_item_id = item['productId']

                    new_product_size_id = item['sizeId']
                    Size.get(Size.id == new_product_size_id)

                    new_product_quantity = item['quantity']
                    product = Product.get(Product.id == new_product_item_id)
                    new_product_price = product.price * new_product_quantity

                    OrderItem.create(order_id=order.id, product_id=new_product_item_id,
                                     size_id=new_product_size_id,
                                     quantity=new_product_quantity, price=new_product_price)

                except Product.DoesNotExist:
                    transaction.rollback()
                    return {'error': 'product not found'}, 404
                except Size.DoesNotExist:
                    transaction.rollback()
                    return {'error': 'size not found'}, 404

            return {'id': order.id}

        except Customer.DoesNotExist:
            transaction.rollback()
            return {'error': 'customer not found'}, 404


@order_bp.route('/orders/<id>', methods=['PUT'])
def update_order(id):
    with db.atomic() as transaction:
        try:
            Order.get(Order.id == id)
            order_items = OrderItem.delete().where(OrderItem.order_id == id)
            order_items.execute()

            items = request.json['items']
            for item in items:
                try:
                    product_item_id = item['productId']

                    product_size_id = item['sizeId']
                    Size.get(Size.id == product_size_id)

                    product_quantity = item['quantity']
                    product = Product.get(Product.id == product_item_id)
                    product_price = product.price * product_quantity

                    OrderItem.create(order_id=id, product_id=product_item_id,
                                     size_id=product_size_id,
                                     quantity=product_quantity, price=product_price)

                except Product.DoesNotExist:
                    transaction.rollback()
                    return {'error': 'product not found'}, 404
                except Size.DoesNotExist:
                    transaction.rollback()
                    return {'error': 'size not found'}, 404

            return Response(status=204)

        except Order.DoesNotExist:
            transaction.rollback()
            return {'error': 'order not found'}, 404


@order_bp.route('/orders/<id>', methods=['DELETE'])
def delete_order(id):
    try:
        order = Order.get(Order.id == id)
        order.delete_instance()

        order_items = OrderItem.delete().where(OrderItem.order_id == id)
        order_items.execute()

        return Response(status=204)

    except Order.DoesNotExist:
        return {'error': 'order not found'}, 404
