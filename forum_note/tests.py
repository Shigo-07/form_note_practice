from django.test import TestCase
from .models import Note,Tag,Comment
from django.contrib.auth import get_user_model

UserModel = get_user_model()
# Create your tests here.
class NoteModelManagerTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            email="test@example.com",
            password="secret",
            python_stuendt=True,
        )

    #