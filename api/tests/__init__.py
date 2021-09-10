import unittest
from unittest import TestCase

import config
from app import create_app

class AppTest(TestCase):
    def setUp(self) -> None:
        self.test_app = create_app(config.TestConfig)

    def test_config(self):
        self.assertFalse(create_app().testing)
        self.assertTrue(self.test_app.testing)

    def test_time(self):
        with self.test_app.test_client() as client:
            self.assertIn('time', client.get('/api/time').json)

    def tearDown(self) -> None:
        pass

# endpoint tests
from tests.test_auth import AuthTest
from tests.test_market import MarketTest

if __name__ == '__main__':
    unittest.main()
