from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Conversation, Message

User = get_user_model()


class MessagingTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(
            username="u1@example.com",
            email="u1@example.com",
            password="pass12345",
            statut=User.Statut.DIPLOME,
        )
        self.u2 = User.objects.create_user(
            username="u2@example.com",
            email="u2@example.com",
            password="pass12345",
            statut=User.Statut.PME,
        )

    def test_send_message_creates_conversation(self):
        self.client.login(username="u1@example.com", password="pass12345")
        url = reverse("conversation_detail", args=[self.u2.id])
        response = self.client.post(url, {"text": "Bonjour"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Conversation.objects.count(), 1)
        conv = Conversation.objects.first()
        self.assertEqual(Message.objects.filter(conversation=conv).count(), 1)
        msg = Message.objects.first()
        self.assertEqual(msg.text, "Bonjour")
        self.assertEqual(msg.sender, self.u1)
