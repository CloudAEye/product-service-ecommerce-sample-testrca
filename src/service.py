from sqlite3 import IntegrityError

from src.models import Product, db


class ProductService:
    def create_product(self, data: dict):
        new_product = Product(name=data['name'], description=data.get('description', ''), price=data['price'],
                              quantity=data['quantity'])
        db.session.add(new_product)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception('Product already exists')
        return {'id': new_product.id}

    def get_all_products(self):
        products: list[Product] = Product.query.all()
        return [{'id': p.id, 'name': p.name, 'description': p.description, 'price': p.price, 'quantity': p.quantity} for
                p
                in products]

    def get_one_product(self, id: int):
        product = Product.query.get(id)
        if product:
            return {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price,
                    'quantity': product.quantity}
        return None

    def update_product(self, product_id: int, data: dict):
        product = Product.query.get(product_id)
        if product:
            product.name = data.get('name', product.name)
            product.description = data.get('description', product.description)
            product.price = data.get('price', product.price)
            product.quantity = data.get('quantity', product.quantity)
            db.session.commit()
            return {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price,
                    'quantity': product.quantity}
        return None

    def delete_product(self, product_id: int):
        # Query.get()
        # method is considered
        # legacy as of
        # the
        # 1.
        # x
        # series
        # of
        # SQLAlchemy and becomes
        # a
        # legacy
        # construct in 2.0.The
        # method is now
        # available as Session.get()(deprecated
        # since: 2.0) (Background on SQLAlchemy 2.0 at: https: // sqlalche.me/e/b8d9)
        # product = Product.query.get(product_id)
        #
        # todo can be a deprecation example
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price,
                    'quantity': product.quantity}
        return None

    def delete_all_products(self):
        result = Product.query.delete()
        print("delerted : ", result)
        return result
