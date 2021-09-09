import unittest
from unittest import TestCase

from flask import json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Session = sessionmaker()  # creates the Session class
engine = create_engine('sqlite:///')

from app import create_app
from app.auth.routes import register

class AuthTest(TestCase):
    def setUp(self) -> None:
        self.connection = engine.connect()
        self.transaction = self.connection.begin()  # creates a "non-ORM" transaction
        self.session = Session(bind=self.connection)
        
        self.test_app = create_app({'TESTING': True})
        self.user_creds = {
            'email': 'authtest@test.net',
            'password': 'admin'
        }

    def test_register(self):
        endpoint = '/auth/register'
        with self.test_app.test_client() as client:
            no_data = client.post(endpoint)
            assert no_data.json['message'] == 'Headers must include registration data.'
            
            # valid = client.post(
            #     endpoint, 
            #     data=json.dumps(self.user_creds),
            #     content_type='application/json'
            # )
            # print(valid.json)
            

    def tearDown(self) -> None:
        self.session.close()
        self.transaction.rollback()  # rolls back the entire session, even commits
        self.connection.close()

if __name__ == '__main__':
    unittest.main()