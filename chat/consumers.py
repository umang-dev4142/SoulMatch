import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message
from accounts.models import Profile


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group = f"chat_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)

        message = data.get("message")

        if not message:
            return

        user = self.scope["user"]

        profile = await sync_to_async(
            Profile.objects.get
        )(user=user)

        saved_message = await self.save_message(
            user,
            message
        )

        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "chat_message",
                "message_id": saved_message.id,
                "message": saved_message.message,
                "username": profile.fullname,
                "user_id": user.id,
                "timestamp": saved_message.timestamp.strftime("%I:%M %p"),
            }
        )

    @sync_to_async
    def save_message(self, user, message):

        room = Room.objects.get(
            id=self.room_id
        )

        return Message.objects.create(
            room=room,
            sender=user,
            message=message
        )

    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                "message_id": event["message_id"],
                "message": event["message"],
                "username": event["username"],
                "user_id": event["user_id"],
                "timestamp": event["timestamp"],
            })
        )