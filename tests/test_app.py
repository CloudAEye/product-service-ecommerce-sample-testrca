import os
import unittest
from typing import Optional

import requests

from src.app import app
from src.config import SQLALCHEMY_DATABASE_URI
from src.service import ProductService


class TestApp(unittest.TestCase):
    service = ProductService()
    username = "test_app@cloudaeye.com"
    password = "Admin@1234"
    access_token: Optional[str] = None
    product = {
            "name": "Product 1",
            "description": "Product 1 Description",
            "price": 9.99,
            "quantity": 10
        }
    product_id: Optional[int] = None

    @classmethod
    def setUpClass(cls):
        app.config['TEST_MODE'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        cls.app = app.test_client()
        user_service_url = os.getenv('USER_SERVICE_URL', '')
        requests.post(f'{user_service_url}/register', json={'username': cls.username, 'password': cls.password})
        login_response = requests.post(f'{user_service_url}/login',
                                       json={'username': cls.username, 'password': cls.password})
        cls.access_token = login_response.json().get("access_token", "")
        with app.app_context():
            print("Clear orphan products from prev runs (if any)")
            ProductService().delete_all_products()

    def test_01_list_products_endpoint_empty_items(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        response = self.app.get('/products', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual([], response.json)

    def test_02_add_product_endpoint(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        response = self.app.post('/products', headers=headers, json=self.product)
        self.assertEqual(response.status_code, 201)
        product_id = response.json.get("id", None)
        self.assertIsNotNone(product_id)

    def test_03_list_products_endpoint_newly_added_items(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        response = self.app.get('/products', headers=headers)
        print(response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_04_update_product_endpoint(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        list_response = self.app.get('/products', headers=headers)
        self.assertEqual(list_response.status_code, 200)
        self.assertGreaterEqual(len(list_response.json), 1)
        product_id = list_response.json[0].get("id", None)
        self.assertIsNotNone(product_id)
        updated_name = self.product.get("name", "") + " updated"
        response = self.app.put(f'/products/{product_id}', headers=headers, json={"name": updated_name})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("name", None), updated_name)

    def test_05_delete_product_endpoint(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        list_response = self.app.get('/products', headers=headers)
        self.assertEqual(list_response.status_code, 200)
        self.assertGreaterEqual(len(list_response.json), 1)
        product_id = list_response.json[0].get("id", None)
        self.assertIsNotNone(product_id)
        delete_response = self.app.delete(f'/products/{product_id}', headers=headers)
        self.assertEqual(delete_response.status_code, 200)

    def test_06_list_products_endpoint_remove_added_items(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        response = self.app.get('/products', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)



if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = None  # None to keep the method definition order
    unittest.TextTestRunner().run(test_loader.loadTestsFromTestCase(TestApp))
