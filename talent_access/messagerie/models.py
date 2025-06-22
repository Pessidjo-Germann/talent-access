from django.db import models
from users.models import Utilisateur


class Conversation(models.Model):
    participant1 = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="conversations_as_participant1",
    )
    participant2 = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="conversations_as_participant2",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["participant1", "participant2"], name="unique_conversation_pair"
            )
        ]

    def save(self, *args, **kwargs):
        # Ensure participant1 id is smaller for uniqueness independent of order
        if self.participant1_id and self.participant2_id and self.participant1_id > self.participant2_id:
            self.participant1, self.participant2 = self.participant2, self.participant1
        super().save(*args, **kwargs)

    def other_participant(self, user):
        if user == self.participant1:
            return self.participant2
        return self.participant1

    def __str__(self):
        return f"Conversation {self.participant1} - {self.participant2}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        Utilisateur, on_delete=models.CASCADE, related_name="sent_messages"
    )
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Message de {self.sender}"
