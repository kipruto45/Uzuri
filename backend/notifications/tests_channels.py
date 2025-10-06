from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification


class NotificationsChannelsTest(TransactionTestCase):
    """Tests that creating a Notification triggers a channel layer group_send.

    This test avoids running a full websocket stack by creating a temporary channel,
    adding it to the expected group, creating a Notification (which triggers the
    signal), and then receiving the message from the in-memory channel layer.
    """

    reset_sequences = True

    def test_notification_signal_push_delivers_channel_message(self):
        User = get_user_model()
        user = User.objects.create_user(email='wsuser@example.com', password='pass')

        group = f"notifications_{user.id}"

        channel_layer = get_channel_layer()

        # Create a temporary channel name and add it to the group
        temp_channel = f"test_channel_{user.id}"
        async_to_sync(channel_layer.group_add)(group, temp_channel)

        # Create a notification - signal should send to group
        notif = Notification.objects.create(
            user=user,
            category='general',
            type='test',
            title='Test Notification',
            message='Hello over channel',
            urgency='info',
            channels=['in_app'],
        )

        # Receive the message from the temporary channel
        message = async_to_sync(channel_layer.receive)(temp_channel)

        # The signal sends a dict with type 'send_notification' and content payload
        self.assertEqual(message.get('type'), 'send_notification')
        content = message.get('content')
        self.assertIsNotNone(content)
        self.assertEqual(content.get('id'), notif.id)
        self.assertEqual(content.get('title'), notif.title)
        self.assertEqual(content.get('message'), notif.message)
        self.assertEqual(content.get('category'), notif.category)

        # Clean up
        async_to_sync(channel_layer.group_discard)(group, temp_channel)
