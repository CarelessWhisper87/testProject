from django.test import TestCase
from .models import Message

class MessageModelTest(TestCase):

    def test_str_method(self):
        msg = Message.objects.create(text="Hello")
        self.assertEqual(str(msg), "Hello")
