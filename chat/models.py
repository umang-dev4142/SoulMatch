from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="room_user1"
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="room_user2"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user1', 'user2'],
                name='unique_room_pair'
            )
        ]

    def __str__(self):
        return f"{self.user1} ↔ {self.user2}"


class Message(models.Model):

    MESSAGE_TYPE = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
    )

    STATUS_TYPE = (
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('seen', 'Seen'),
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField(blank=True, null=True)

    image = models.ImageField(
        upload_to='chat_images/',
        blank=True,
        null=True
    )

    # 🔥 NEW FEATURES
    message_type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPE,
        default='text'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_TYPE,
        default='sent'
    )

    is_seen = models.BooleanField(default=False)

    is_edited = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)

    edited_at = models.DateTimeField(auto_now=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} → {self.room}"