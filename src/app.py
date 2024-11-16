from typing import Optional

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from src.models import db
from src.service import ProductService

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

jwt = JWTManager(app)


@app.before_request
def create_tables():
    # The following line will remove this handler, making it
    # only run on the first request
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()


@app.route('/products', methods=['POST'])  # Create
@jwt_required()
def create_product():
    try:
        data = request.json
        product_service = ProductService()
        new_product = product_service.create_product(data)
        return jsonify(new_product), 201
    except Exception as e:
        return jsonify({'message': e}), 400


@app.route('/products', methods=['GET'])  # Read
@jwt_required()
def get_products():
    try:
        # Lists all products
        product_service = ProductService()
        all_products = product_service.get_all_products()
        return jsonify(all_products), 200
    except Exception as e:
        return jsonify({'message': e}), 400


@app.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product_by_id(product_id):
    try:
        product_service = ProductService()
        one_product: Optional[dict] = product_service.get_one_product(product_id)
        if one_product:
            return jsonify(one_product), 200
        else:
            return jsonify({'message': 'No product found with given id'}), 404
    except Exception as e:
        return jsonify({'message': e}), 400


@app.route('/products/<int:product_id>', methods=['PUT'])  # Update
@jwt_required()
def update_product(product_id):
    try:
        # Fetch data from payload
        data = request.json
        product_service = ProductService()
        # Fetch the product
        one_product = product_service.update_product(product_id, data)
        if one_product:
            return jsonify(one_product), 200
        else:
            return jsonify({'message': 'No product found with given id'}), 404
    except Exception as e:
        return jsonify({'message': e}), 500


@app.route('/products/<int:product_id>', methods=['DELETE'])  # Delete
@jwt_required()
def delete_product(product_id):
    try:
        product_service = ProductService()
        one_product = product_service.delete_product(product_id)
        if one_product:
            return jsonify(one_product), 200
        else:
            return jsonify({'message': 'No product found with given id'}), 404
    except Exception as e:
        return jsonify({'message': e}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5001)
