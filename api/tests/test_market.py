import config
import unittest
from unittest import TestCase
from flask import json
from app import create_app, db
from app.market.models import Product

class MarketTest(TestCase):

    def setUp(self) -> None:
        self.test_app = create_app(config.TestConfig)
        db.create_all(app=self.test_app)

    def test_market(self):
        endpoint = '/market/'
        with self.test_app.test_client() as client:
            
            
            
            valid = client.get(endpoint)
            

    def tearDown(self) -> None:
        db.drop_all(app=self.test_app)


if __name__ == '__main__':
    unittest.main()
