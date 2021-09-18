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
        self.mock_product_price = 3.50
        self.mock_product_seller_id = 1
        db.create_all(app=self.test_app)

    def test_all(self) -> None:
        endpoint = '/products/'

        with self.test_app.test_client() as client:
            # populate db with products to test against
            with self.test_app.app_context():
                products = []
                for i in range(1, 11):
                    product = Product(id=i,
                                      name=self.mock_product_name,
                                      is_active=True)
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

    def test_one(self) -> None:
        with self.test_app.test_client() as client:
            id = 1
            endpoint = f'/products/{id}'

            # can only get products in the database
            nonexistent = client.get(endpoint).json
            self.assertEqual(nonexistent['status'], 500)

            # can successfully get a product from the database
            with self.test_app.app_context():
                product = Product(id=id,
                                  name=self.mock_product_name,
                                  is_active=True)
                db.session.add(product)
                db.session.commit()

            valid = client.get(endpoint).json
            self.assertEqual(valid['status'], 200)

            # response includes correct product data
            self.assertIn('product', valid)
            product_data = valid['product']
            self.assertEqual(product_data['id'], id)
            self.assertEqual(product_data['name'], self.mock_product_name)

            # cannot get an inactive product from the database
            id = 2
            endpoint = f'/products/{id}'

            with self.test_app.app_context():
                inactive = Product(id=id,
                                   name=self.mock_product_name,
                                   is_active=False)
                db.session.add(inactive)
                db.session.commit()

            invalid = client.get(endpoint).json
            self.assertEqual(invalid['status'], 500)

    def test_sell(self) -> None:
        endpoint = '/products/sell'

        with self.test_app.test_client() as client:
            # no empty requests
            no_data = client.post(endpoint).json
            self.assertEqual(no_data['status'], 500)

            # request with no name will fail
            no_name_product = {
                'price': self.mock_product_price,
                'seller_id': self.mock_product_seller_id
            }
            no_name = client.post(endpoint,
                                  data=json.dumps(no_name_product),
                                  content_type='application/json').json
            self.assertEqual(no_name['status'], 500)

            # request with no price will fail
            no_price_product = {
                'name': self.mock_product_name,
                'seller_id': self.mock_product_seller_id
            }
            no_price = client.post(endpoint,
                                   data=json.dumps(no_price_product),
                                   content_type='application/json').json
            self.assertEqual(no_price['status'], 500)

            # request with no seller id will fail
            no_seller_product = {
                'name': self.mock_product_name,
                'price': self.mock_product_price
            }
            no_seller = client.post(endpoint,
                                    data=json.dumps(no_seller_product),
                                    content_type='application/json').json
            self.assertEqual(no_seller['status'], 500)

            # seller id must belong to registered user
            valid_product = {
                'name': self.mock_product_name,
                'price': 3.50,
                'seller_id': 1
            }
            unregistered = client.post(endpoint,
                                       data=json.dumps(valid_product),
                                       content_type='application/json').json
            self.assertEqual(unregistered['status'], 500)

            # request with product name, price, and registered seller ID is accepted
            with self.test_app.app_context():
                user = User(
                    id=self.mock_product_seller_id)  # just id is needed
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

    def test_deactivate(self) -> None:
        with self.test_app.test_client() as client:
            id = 1
            endpoint = f'products/deactivate/{id}'

            print('testing deactivate...')
            print('testing empty endpoint...')
            # no empty requests
            no_data = client.post(endpoint).json
            self.assertEqual(no_data['status'], 500)

            print('testing unregistered product...')
            # can't deactivate a product not in the database
            valid_request = {'user_id': self.mock_product_seller_id}
            not_stored = client.post(endpoint,
                                     data=json.dumps(valid_request),
                                     content_type='application/json').json
            self.assertEqual(not_stored['status'], 500)

            # create a product in the db to test against
            with self.test_app.app_context():
                # a registered user has to exist to create the product
                user = User(
                    id=self.mock_product_seller_id)  # just id is needed
                db.session.add(user)

                product = Product(id=id,
                                  name=self.mock_product_name,
                                  seller_id=user.id,
                                  is_active=True)
                db.session.add(product)
                db.session.commit()

            # cannot change product if seller_id != user_id
            invalid_request = {'user_id': self.mock_product_seller_id + 1}
            invalid = client.post(endpoint,
                                  data=json.dumps(invalid_request),
                                  content_type='application/json').json
            self.assertEqual(invalid['status'], 500)

            # can successfully deactivate a product if all conditions met
            valid = client.post(endpoint,
                                data=json.dumps(valid_request),
                                content_type='application/json').json
            self.assertEqual(valid['status'], 200)

            # cannot deactivate an already deactivated product
            repeat = client.post(endpoint,
                                 data=json.dumps(valid_request),
                                 content_type='application/json').json
            self.assertEqual(repeat['status'], 500)

    def tearDown(self) -> None:
        db.drop_all(app=self.test_app)


if __name__ == '__main__':
    unittest.main()
