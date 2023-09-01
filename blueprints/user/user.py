from flask import Blueprint, request, Response
from models import *

user_bp = Blueprint('user', __name__)


@user_bp.route('/users', methods=['POST'])
def register_user():
    try:
        user = User.create(name=request.json['name'], surname=request.json['surname'], city=request.json['city'],
                           telephone=request.json['telephone'], email=request.json['email'])

        Customer.create(user_id=user.id)

        return {'id': user.id}

    except IntegrityError:
        return {'error': 'invalid telephone or email'}


@user_bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.get(User.id == id)
        user.name = request.json['name']
        user.surname = request.json['surname']
        user.city = request.json['city']
        user.telephone = request.json['telephone']
        user.email = request.json['email']
        user.save()

        return Response(status=204)

    except User.DoesNotExist:
        return {'error': 'user not found'}, 404

    except IntegrityError:
        return {'error': 'invalid telephone or email'}


@user_bp.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.get(User.id == id)
        user.delete_instance()

        customer = Customer.get(Customer.user_id == id)
        customer.delete_instance()

        return Response(status=204)

    except User.DoesNotExist:
        return {'error': 'user not found'}, 404
