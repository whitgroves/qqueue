import config
import unittest
from unittest import TestCase
from flask import json
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.auth.models import User


class AuthTest(TestCase):
    def setUp(self) -> None:
        self.test_app = create_app(config.TestConfig)
        db.create_all(app=self.test_app)

    def test_register(self):
        endpoint = '/auth/register'
        with self.test_app.test_client() as client:
            no_data = client.post(endpoint).json
            self.assertEqual(no_data['status'], 500)

            user_creds = {
                'email': 'test_register@localhost',
                'password': 'admin'
            }

            valid = client.post(endpoint,
                                data=json.dumps(user_creds),
                                content_type='application/json').json
            self.assertEqual(valid['status'], 200)

            duplicate = client.post(endpoint,
                                    data=json.dumps(user_creds),
                                    content_type='application/json').json
            self.assertEqual(duplicate['status'], 500)

    def test_login(self):
        endpoint = '/auth/login'
        with self.test_app.test_client() as client:
            no_data = client.post(endpoint).json
            self.assertEqual(no_data['status'], 500)

            user_creds = {'email': 'test_login@localhost', 'password': 'admin'}

            # this is not guaranteed to run after register so we must setup a user first
            with self.test_app.app_context():
                user = User(id=1,
                            email=user_creds['email'],
                            password_hash=generate_password_hash(
                                user_creds['password']))
                db.session.add(user)
                db.session.commit()

            bad_creds = {**user_creds}  # immutability matters
            bad_creds['password'] = 'wrong'
            bad_pair = client.post(endpoint,
                                   data=json.dumps(bad_creds),
                                   content_type='application/json').json
            self.assertEqual(bad_pair['status'], 500)

            valid = client.post(endpoint,
                                data=json.dumps(user_creds),
                                content_type='application/json').json
            self.assertEqual(valid['status'], 200)
            self.assertIn('token', valid)

    def tearDown(self) -> None:
        db.drop_all(app=self.test_app)


if __name__ == '__main__':
    unittest.main()
