from django.test import TestCase
from django.test import Client
from .models import Note
from django.contrib.auth.models import User
import json
from .serializers import NoteSerializer

# Create your tests here.
class NoteApiTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user1", "user1@gmail.com", "user1")
        note = Note(text="abcd", priority=10, user=self.user)
        note.save()

        note = Note(text="for delete", priority=20, user=self.user)
        note.save()

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

    def test_get_list(self):
        response = Client().get("/notes/api", **self.auth_headers)
        notes = NoteSerializer(Note.objects.filter(user=self.user.id), many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), notes)

    def test_fail_get_list_unauthorized(self):
        expected_content = {'detail': 'Authentication credentials were not provided.'}
        response = Client().get("/notes/api")

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)

    def test_get(self):
        response = Client().get("/notes/api/1", **self.auth_headers)
        note = NoteSerializer(Note.objects.get(id=response.data["id"], user=self.user.id)).data

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), note)

    def test_fail_get_unauthorized(self):
        expected_content = {'detail': 'Authentication credentials were not provided.'}
        response = Client().get("/notes/api/1")

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)

    def test_update(self):
        update_note = { 'text': "new text" }

        response = Client().put("/notes/api/1", update_note, **self.auth_headers, content_type="application/json")
        note = NoteSerializer(Note.objects.get(id=response.data['id'])).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(note["text"], update_note["text"])
        self.assertJSONEqual(str(response.content, encoding="utf8"), note)

    def test_update_many(self):
        update_note = { 'text': "new text", 'priority': 200 }

        response = Client().put("/notes/api/1", update_note, **self.auth_headers, content_type="application/json")
        note = NoteSerializer(Note.objects.get(id=response.data['id'])).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(note["text"], update_note["text"])
        self.assertEqual(note["priority"], update_note["priority"])
        self.assertJSONEqual(str(response.content, encoding="utf8"), note)

    def test_update_unallowed(self):
        update_note = { 'user': 15, 'timestamp': "10" }

        response = Client().put("/notes/api/1", update_note, **self.auth_headers, content_type="application/json")
        note = NoteSerializer(Note.objects.get(id=response.data['id'])).data

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(note["user"], update_note["user"])
        self.assertNotEqual(note["timestamp"], update_note["timestamp"])
        self.assertJSONEqual(str(response.content, encoding="utf8"), note)

    def test_fail_update_unauthorized(self):
        update_note = { 'text': "new text" }
        expected_content = {'detail': 'Authentication credentials were not provided.'}

        response = Client().put("/notes/api/1", update_note, content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)

    def test_delete(self):
        response = Client().delete("/notes/api/2", **self.auth_headers)
        expected_content = {"res": "Object deleted!"}

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)

    def test_fail_delete_unauthorized(self):
        expected_content = {'detail': 'Authentication credentials were not provided.'}
        response = Client().delete("/notes/api/2")

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_content)
