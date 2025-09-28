from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.group_name = f"notifications_{self.scope['user'].id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Optionally handle client messages
        pass

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["content"]))

    @database_sync_to_async
    def get_unread_count(self):
        return Notification.objects.filter(user=self.scope["user"], is_read=False).count()
