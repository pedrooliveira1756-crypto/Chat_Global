from django.db import models


class user(models.Model):
    username = models.CharField(max_length=100)
    token_hash = models.CharField(max_length=64, blank=True, default='')

    def __str__(self):
        return self.username


class Message(models.Model):
    user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    content = models.TextField()

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"
