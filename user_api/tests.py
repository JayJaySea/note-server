from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import json

# Create your tests here.
class UserApiTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser("admin", "admin@gmail.com", "admin")
        User.objects.create_user("user1", "user1@gmail.com", "user1")

    def test_register(self):
        new_user = {
            "username": "user2",
            "email": "user2@gmail.com",
            "password": "user2" 
        }

        expected_content = {
            "username":"user2",
            "email":"user2@gmail.com"
        }

        c = Client()
        response = c.post("/users/api/register", new_user)

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)

    def test_register_same_username(self):
        new_user = {
            "username": "user1",
            "email": "user3@gmail.com",
            "password": "user3" 
        }

        expected_content = {"detail":"User already exists!"}

        c = Client()
        response = c.post("/users/api/register", new_user)

        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)

    def test_login(self):
        user = { "username": "user1", "password": "user1" }
        response = Client().post("/users/api/login", user)

        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        user = { "username": "user1", "password": "user1" }
        expected_content = { "username": "user1", "email": "user1@gmail.com" }

        c = Client()
        token = json.loads(c.post("/users/api/login", user).content)
        auth_headers = { 'HTTP_AUTHORIZATION': 'Bearer ' + token["access"] }
        response = c.get("/users/api/profile", user, **auth_headers)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)

    def test_delete_profile(self):
        user = { "username": "user1", "password": "user1" }
        expected_content = { "res": "Object deleted!" }

        c = Client()
        token = json.loads(c.post("/users/api/login", user).content)
        auth_headers = { 'HTTP_AUTHORIZATION': 'Bearer ' + token["access"] }
        response = c.delete("/users/api/profile", user, **auth_headers)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)
