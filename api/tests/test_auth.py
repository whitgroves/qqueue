import os
import unittest
from unittest import TestCase
from flask import json
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker

import config
from app import create_app, db

class AuthTest(TestCase):

    def setUp(self) -> None:
        self.test_app = create_app(config.TestConfig)
        db.create_all(app=self.test_app)
        self.user_creds = {
            'email': 'authtest@test.net',
            'password': 'admin'
        }

    def test_register(self):
        endpoint = '/auth/register'
        with self.test_app.test_client() as client:
            no_data = client.post(endpoint)
            self.assertEqual(no_data.json['message'], 'Headers must include registration data.')
            
            valid = client.post(
                endpoint, 
                data=json.dumps(self.user_creds),
                content_type='application/json'
            )
            self.assertEqual(valid.json['message'], 'User registered successfully.')
            
            duplicate = client.post(
                endpoint, 
                data=json.dumps(self.user_creds),
                content_type='application/json'
            )
            self.assertEqual(duplicate.json['message'], 'An account is already registered to that email.')


    def tearDown(self) -> None:
        db.drop_all(app=self.test_app)


if __name__ == '__main__':
    unittest.main()