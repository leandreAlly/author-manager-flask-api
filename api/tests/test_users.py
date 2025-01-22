import json
from api.utils.test_base import BaseTestCase
from api.models.users import User
from datetime import datetime
import unittest


class TestUsers(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create test user
        self.test_user1 = User(
            email="test@example.com",
            username="testuser",
            password=User.generate_hash("password123"),
            is_verified=True
        )
        self.test_user2 = User(
            email="kunal.relan123@gmail.com",
            username="helloworld",
            password=User.generate_hash("password123"),
        )
        

        self.test_user1.create()
        self.test_user2.create()

    def test_login_user(self):
        user = {
            "email": "test@example.com",
            "password": "password123"
        }
        response = self.client.post(
            '/api/users/login',
            data=json.dumps(user),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('access_token' in data)

    def test_login_user_wrong_credential(self):
        user = {
          "email" : "kunal.relan12@gmail.com",
          "password" : "helloworld12"
        }

        response = self.client.post(
            '/api/users/login',
            data = json.dumps(user),
            content_type = 'application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)
    
    def test_login_unverfied_user(self):
        user = {
          "email" : "kunal.relan123@gmail.com",
          "password" : "helloworld"
        }

        response = self.client.post(
            '/api/users/login',
            data = json.dumps(user),
            content_type = 'application/json'
        )
        data = json.dumps(user),
        self.assertEqual(400, response.status_code)

if __name__ == '__main__':
    unittest.main()

