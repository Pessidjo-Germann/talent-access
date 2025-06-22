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

    def test_message_marked_read_when_viewed(self):
        conv = Conversation.objects.create(participant1=self.u1, participant2=self.u2)
        msg = Message.objects.create(conversation=conv, sender=self.u1, text="Hi")
        self.assertFalse(msg.is_read)

        self.client.login(username="u2@example.com", password="pass12345")
        url = reverse("conversation_detail", args=[self.u1.id])
        self.client.get(url)
        msg.refresh_from_db()
        self.assertTrue(msg.is_read)

    def test_unread_count_in_list_view(self):
        conv = Conversation.objects.create(participant1=self.u1, participant2=self.u2)
        Message.objects.create(conversation=conv, sender=self.u2, text="Salut")

        self.client.login(username="u1@example.com", password="pass12345")
        response = self.client.get(reverse("conversation_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["conversations"][0].unread_count, 1)
