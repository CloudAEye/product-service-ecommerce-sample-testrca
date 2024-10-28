import unittest

from src.app import app
from src.config import SQLALCHEMY_DATABASE_URI
from src.service import ProductService


class TestProductService(unittest.TestCase):
    service = ProductService()
    username = "test_service@cloudaeye.com"
    password = "Admin@1234"
    products = [{
        "name": "Product 1",
        "description": "Product 1 Description",
        "price": 9.99,
        "quantity": 10
    }, {
        "name": "Product 2",
        "description": "Product 2 Description",
        "price": 5.99,
        "quantity": 20
    }]
    added_products: list[dict] = []

    @classmethod
    def setUpClass(cls):
        print("setting up")
        app.config['TEST_MODE'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        cls.app = app.test_client()
        # with app.app_context():
        #     print("Delete all products")
        #     cls.service.delete_all_products()

    @classmethod
    def tearDownClass(cls):
        print("tearing down")
        with app.app_context():
            for p in cls.added_products:
                cls.service.delete_product(p.get("id", -1))

    def test_01_add_products(self):
        with app.app_context():
            for product in self.products:
                result = self.service.create_product(product)
                if result and "id" in result:
                    product["id"] = result.get("id", -1)
                    self.added_products.append(product)
            print(self.added_products)
            self.assertEqual(len(self.added_products), len(self.products))

    def test_02_list_products(self):
        with app.app_context():
            result = self.service.get_all_products()
            self.assertEqual(len(result), len(self.added_products))

    def test_03_get_one_product(self):
        with app.app_context():
            for product in self.added_products:
                result = self.service.get_one_product(product.get("id", -1))
                self.assertIn(result, self.added_products)

    def test_04_fetch_none_for_invalid_product(self):
        with app.app_context():
            result = self.service.get_one_product(-1)
            self.assertIsNone(result)

    def test_05_update_product_name(self):
        with app.app_context():
            product = self.products[0]
            product['name'] = product.get("name", "") + " updated"
            result = self.service.update_product(product.get("id", -1), product)
            self.assertIsNotNone(result)
            updated_product = self.service.get_one_product(product.get("id", -1))
            self.assertEqual(updated_product.get("name", ""), product.get("name", ""))

    def test_06_no_update_for_invalid_product(self):
        with app.app_context():
            product = self.products[0]
            updated_name = product.get("name", "") + " updated"
            result = self.service.update_product(-1, {"name": updated_name})
            self.assertIsNone(result)
            not_updated_product = self.service.get_one_product(product.get("id", -1))
            self.assertEqual(not_updated_product.get("name", ""), product.get("name", ""))

    def test_07_delete_one_product(self):
        with app.app_context():
            product = self.added_products[0]
            result = self.service.delete_product(product.get("id", -1))
            self.assertEqual(result, product)
            deleted_product = self.service.get_one_product(product.get("id", -1))
            self.assertIsNone(deleted_product)

    def test_08_no_delete_for_invalid_product(self):
        with app.app_context():
            result = self.service.delete_product(-1)
            self.assertIsNone(result)

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = None  # None to keep the method definition order
    unittest.TextTestRunner().run(test_loader.loadTestsFromTestCase(TestProductService))
