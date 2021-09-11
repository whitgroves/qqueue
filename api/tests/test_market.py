import config
import unittest
from unittest import TestCase
from app import create_app, db
from app.market.models import Product


class MarketTest(TestCase):
    def setUp(self) -> None:
        self.test_app = create_app(config.TestConfig)
        db.create_all(app=self.test_app)

    def test_buy(self):
        with self.test_app.test_client() as client:
            products = []
            for i in range(1, 11):
                product = Product(id=i, name=f'Product {i}')
                products.append(product)

            with self.test_app.app_context():
                db.session.add_all(products)
                db.session.commit()

            all_products = client.get('/market/').json
            self.assertIn('products', all_products)
            self.assertEqual(10, len(all_products['products']))
            
            all_products_dup = client.get('/market/').json
            self.assertDictEqual(all_products, all_products_dup)

    def tearDown(self) -> None:
        db.drop_all(app=self.test_app)


if __name__ == '__main__':
    unittest.main()
