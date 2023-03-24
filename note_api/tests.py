from django.test import TestCase
from django.test import Client
from .models import Note
from django.contrib.auth.models import User
import json
from django.utils import timezone

# Create your tests here.
class NoteApiTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("user1", "user1@gmail.com", "user1")

    def test_create(self):
        pass

    def test_fail_create_unauthorized(self):
        pass

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
