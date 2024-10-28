import os

from flask_sqlalchemy import SQLAlchemy

from src.config import TEST_MODE

db = SQLAlchemy()

class Product(db.Model):
    # __tablename__ = "product_test" if TEST_MODE else "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)