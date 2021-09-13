import config
import unittest
from unittest import TestCase
from flask import json
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.auth.models import User
from app.utils.web import dev_token


class AuthTest(TestCase):
    def setUp(self) -> None:
        self.test_app = create_app(config.TestConfig)
        db.create_all(app=self.test_app)

    def test_check_token(self) -> None:
        endpoint = '/auth/'

        with self.test_app.test_client() as client:
            # no empty requests
            no_data = client.post(endpoint).json
            self.assertEqual(no_data['status'], 500)

            # token must be correct
            bad_auth = {'token': dev_token + 'anything', 'id': 1}
            invalid = client.post(endpoint,
                                  data=json.dumps(bad_auth),
                                  content_type='application/json').json
            self.assertEqual(invalid['status'], 500)

            # request must include user data
            partial_auth = {'token': dev_token}
            no_id = client.post(endpoint,
                                data=json.dumps(partial_auth),
                                content_type='application/json').json
            self.assertEqual(no_id['status'], 500)

            # user making request must be in database
            valid_auth = {'token': dev_token, 'id': 1}
            no_user = client.post(endpoint,
                                  data=json.dumps(valid_auth),
                                  content_type='application/json').json
            self.assertEqual(no_user['status'], 500)

            # valid request is accepted by the server
            valid_creds = {
                'email': 'test_login@localhost',
                'password': 'admin'
            }
            with self.test_app.app_context():
                user = User(id=1,
                            email=valid_creds['email'],
                            password_hash=generate_password_hash(
                                valid_creds['password']))
                db.session.add(user)
                db.session.commit()

            valid = client.post(endpoint,
                                data=json.dumps(valid_auth),
                                content_type='application/json').json
            self.assertEqual(valid['status'], 200)

    def test_register(self) -> None:
        endpoint = '/auth/register'

        with self.test_app.test_client() as client:
            # no empty requests
            no_data = client.post(endpoint).json
            self.assertEqual(no_data['status'], 500)

            # user can register with valid credentials
            valid_creds = {
                'email': 'test_register@localhost',
                'password': 'admin'
            }
            valid = client.post(endpoint,
                                data=json.dumps(valid_creds),
                                content_type='application/json').json
            self.assertEqual(valid['status'], 200)

            # the same user cannot be registered twice
            duplicate = client.post(endpoint,
                                    data=json.dumps(valid_creds),
                                    content_type='application/json').json
            self.assertEqual(duplicate['status'], 500)

    def test_login(self) -> None:
        endpoint = '/auth/login'

        with self.test_app.test_client() as client:
            # no empty requests
            no_data = client.post(endpoint).json
            self.assertEqual(no_data['status'], 500)

            # create a user to test against
            valid_creds = {
                'email': 'test_login@localhost',
                'password': 'admin'
            }
            with self.test_app.app_context():
                user = User(id=1,
                            email=valid_creds['email'],
                            password_hash=generate_password_hash(
                                valid_creds['password']))
                db.session.add(user)
                db.session.commit()

            # request must include correct password
            bad_creds = {**valid_creds}  # immutability matters
            bad_creds['password'] = 'wrong'
            bad_pair = client.post(endpoint,
                                   data=json.dumps(bad_creds),
                                   content_type='application/json').json
            self.assertEqual(bad_pair['status'], 500)

            # correct credentials can login
            valid = client.post(endpoint,
                                data=json.dumps(valid_creds),
                                content_type='application/json').json
            self.assertEqual(valid['status'], 200)
            self.assertIn('token', valid)

            # confirm endpoint is hashing submitted passwords
            unhashed_creds = {
                'email': 'unhashed@localhost',
                'password': 'admin'
            }
            with self.test_app.app_context():
                unhashed = User(id=2,
                                email=unhashed_creds['email'],
                                password_hash=unhashed_creds['password'])
                db.session.add(unhashed)
                db.session.commit()

            wrong_pass = client.post(endpoint,
                                     data=json.dumps(unhashed_creds),
                                     content_type='application/json').json
            self.assertEqual(wrong_pass['status'], 500)

    def tearDown(self) -> None:
        db.drop_all(app=self.test_app)


if __name__ == '__main__':
    unittest.main()
