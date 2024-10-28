import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    @staticmethod
    def get_table_name():
        if os.getenv('TEST_MODE', 'FALSE') == 'TRUE':
            return 'product_test'
        return 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Set __tablename__ dynamically based on the environment
    __table_args__ = {'extend_existing': True}
    __tablename__ = get_table_name()
