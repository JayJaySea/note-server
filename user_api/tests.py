from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .serializers import UserDetailsSerializer
import json

# Create your tests here.
class UserApiTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser("admin", "admin@gmail.com", "admin")
        User.objects.create_user("user1", "user1@gmail.com", "user1")

        user = {"username": "user1", "password": "user1"}
        client = Client()

        token = json.loads(client.post("/users/api/login", user).content)
        self.auth_headers = { 'HTTP_AUTHORIZATION': 'Bearer ' + token["access"] }

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

        response = Client().post("/users/api/register", new_user)

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)

    def test_fail_register_same_username(self):
        new_user = {
            "username": "user1",
            "email": "user3@gmail.com",
            "password": "user3" 
        }
        expected_content = {"detail":"User already exists!"}

        response = Client().post("/users/api/register", new_user)

        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)

    def test_profile(self):
        expected_content = { "username": "user1", "email": "user1@gmail.com" }

        response = Client().get("/users/api/profile", **self.auth_headers)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)

    def update_profile(self):
        update_user = { "username": "updatedUser" }

        response = Client().put("/users/api/profile", update_user, **self.auth_headers)
        note = UserDetailsSerializer(User.objects.get(id=response.data['id'])).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(update_user["username"], note["username"])

    def update_profile_many(self):
        update_user = { "username": "updatedUser", "email": "email@gmail.com" }

        response = Client().put("/users/api/profile", update_user, **self.auth_headers)
        note = UserDetailsSerializer(User.objects.get(id=response.data['id'])).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(update_user["username"], note["username"])
        self.assertEqual(update_user["email"], note["email"])

    def test_delete_profile(self):
        expected_content = { "res": "Object deleted!" }

        response = Client().delete("/users/api/profile", **self.auth_headers)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)
