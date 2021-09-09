import unittest
from unittest import TestCase

from app import create_app

class AppTest(TestCase):
    def setUp(self) -> None:
        self.test_app = create_app({'TESTING': True})

    def test_config(self):
        assert not create_app().testing
        assert self.test_app.testing

    def test_time(self):
        with self.test_app.test_client() as client:
            assert 'time' in client.get('/api/time').json

    def tearDown(self) -> None:
        pass

from tests.test_auth import AuthTest

if __name__ == '__main__':
    unittest.main()
