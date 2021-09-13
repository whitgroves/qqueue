import config
import unittest
from unittest import TestCase
from flask import json
from app import create_app, db
from app.products.models import Product
from app.auth.models import User


class ProductsTest(TestCase):
    def setUp(self) -> None:
        self.test_app = create_app(config.TestConfig)
        self.mock_product_name = 'Test Product'
        db.create_all(app=self.test_app)

    def test_all(self):
        endpoint = '/products/'

        with self.test_app.test_client() as client:
            # populate db with products to test against
            with self.test_app.app_context():
                products = []

                for i in range(1, 11):
                    product = Product(id=i, name=self.mock_product_name)
                    products.append(product)

                db.session.add_all(products)
                db.session.commit()

            # we should get everything from the db
            all_products = client.get(endpoint).json
            self.assertIn('products', all_products)
            self.assertEqual(len(all_products['products']), 10)

            # repeat calls should produce the same result
            all_products_dup = client.get(endpoint).json
            self.assertDictEqual(all_products_dup, all_products)

    def test_one(self):
        id = 1
        endpoint = f'/products/{id}'

        with self.test_app.test_client() as client:
            # can only get products in the database
            nonexistent = client.get(endpoint).json
            self.assertEqual(nonexistent['status'], 500)

            # can successfully get a product from the database
            with self.test_app.app_context():
                product = Product(id=id, name=self.mock_product_name)
                db.session.add(product)
                db.session.commit()

            valid = client.get(endpoint).json
            self.assertEqual(valid['status'], 200)

            # response includes correct product data
            self.assertIn('product', valid)
            product_data = valid['product']
            self.assertEqual(product_data['id'], id)
            self.assertEqual(product_data['name'], self.mock_product_name)

    def test_sell(self):
        endpoint = '/products/sell'

        with self.test_app.test_client() as client:
            # no empty requests
            no_data = client.post(endpoint).json
            self.assertEqual(no_data['status'], 500)

            # request with just a product name will fail
            name_only = {'name': self.mock_product_name}
            no_seller = client.post(endpoint,
                                    data=json.dumps(name_only),
                                    content_type='application/json').json
            self.assertEqual(no_seller['status'], 500)

            # seller id must belong to registered user
            valid_product = {'name': self.mock_product_name, 'seller_id': 1}
            unregistered = client.post(endpoint,
                                       data=json.dumps(valid_product),
                                       content_type='application/json').json
            self.assertEqual(unregistered['status'], 500)

            # request with product name and registered seller ID is accepted
            with self.test_app.app_context():
                user = User(id=1)  # just id is needed
                db.session.add(user)
                db.session.commit()
            valid = client.post(endpoint,
                                data=json.dumps(valid_product),
                                content_type='application/json').json
            self.assertEqual(valid['status'], 200)

            # response includes correct product data
            self.assertIn('product', valid)
            product_data = valid['product']
            self.assertIn('id', product_data)  # just check we got one back
            self.assertEqual(product_data['name'], self.mock_product_name)

            # confirm product was added to the db
            with self.test_app.app_context():
                in_db = db.session.query(Product).get(product_data['id'])
                self.assertIsNotNone(in_db)

    def tearDown(self) -> None:
        db.drop_all(app=self.test_app)


if __name__ == '__main__':
    unittest.main()
