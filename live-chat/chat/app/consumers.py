# app/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class TextRoomConsumer(WebsocketConsumer):
    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group

        # Async to Sync Translation: async_to_sync is necessary because the Django Channels layer (which manages groups and messages) operates asynchronously
        # but your consumer methods are synchronous
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        text = text_data_json['text']
        sender = text_data_json['sender']
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text,
                'sender': sender
            }
        )

    def chat_message(self, event):
        # Receive message from room group
        text = event['message']
        sender = event['sender']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'text': text,
            'sender': sender
        }))

# Timeline of WebSocket Communication in Django Channels

# 1. User Connects to the WebSocket
# Event: A user navigates to a chat room in the web application.
# Action: The browser establishes a WebSocket connection to the server.
# Django Channels: The connect method of the TextRoomConsumer class is triggered.
    # The connect method:
    # Extracts the room_name from the URL.
    # Creates a room_group_name based on the room_name.
    # Adds the user's WebSocket connection to the corresponding group using self.channel_layer.group_add.
    # Accepts the WebSocket connection with self.accept().
    # Outcome: The user's WebSocket connection is now part of a group (chat room) and ready to send/receive messages.

# 2. User Sends a Message
# Event: The user types a message and sends it through the WebSocket.
# Action: The WebSocket client sends the message data to the server.
# Django Channels: The receive method of the TextRoomConsumer class is triggered.
    # The receive method:
    # Parses the incoming JSON message.
    # Extracts the text (message) and sender (user who sent the message).
    # Sends the message to the entire group using self.channel_layer.group_send.
    # The event dictionary includes 'type': 'chat_message', which tells Django Channels which method to call when the message is received by the group.

# 3. Django Channels Distributes the Message
# Event: The group_send method sends the message to the group.
# Action: Django Channels distributes the message to all WebSocket connections in the group.
# Django Channels: For each WebSocket connection in the group, Django Channels looks at the type field in the event dictionary.
#    Since the type is 'chat_message', Django Channels automatically calls the chat_message method on each connection in the group.

# 4. Users Receive the Message
# Event: Each WebSocket connection in the group receives the message.
# Action: The chat_message method is triggered on each connected user's consumer.
# Django Channels: The chat_message method:
# Extracts the text and sender from the event dictionary.
# Sends the message data back to the WebSocket client (the user's browser) using self.send().
# Outcome: All users in the chat room see the new message appear in real-time.
# 5. User Disconnects
# Event: A user closes the chat room or navigates away, closing the WebSocket connection.
# Action: The WebSocket connection is terminated.
# Django Channels: The disconnect method of the TextRoomConsumer class is triggered.
# The disconnect method:
# Removes the user's WebSocket connection from the group using self.channel_layer.group_discard.
# Outcome: The user is no longer part of the chat room, and their WebSocket connection is closed.
