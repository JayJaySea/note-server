from django.test import TestCase
from django.test import Client
from .models import Note
from django.contrib.auth.models import User
import json
from .serializers import NoteSerializer

# Create your tests here.
class NoteApiTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("user1", "user1@gmail.com", "user1")

        user = {"username": "user1", "password": "user1"}
        client = Client()

        token = json.loads(client.post("/users/api/login", user).content)
        self.auth_headers = { 'HTTP_AUTHORIZATION': 'Bearer ' + token["access"] }

    def test_create(self):
        new_note = { "text": "abcd", "priority": 20 }

        response = Client().post("/notes/api", new_note , **self.auth_headers)
        note = NoteSerializer(Note.objects.get(id=response.data['id'])).data

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(str(response.content, encoding="utf8"), note)


    def test_fail_create_unauthorized(self):
        new_note = { "text": "abcd", "priority": 20 }
        expected_content = {'detail': 'Authentication credentials were not provided.'}

        response = Client().post("/notes/api", new_note)

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)

    def test_get(self):
        pass

    def test_fail_get_unauthorized(self):
        pass

    def test_update(self):
        pass

    def test_fail_update_unauthorized(self):
        pass

    def test_delete(self):
        pass

    def test_fail_delete_unauthorized(self):
        pass
