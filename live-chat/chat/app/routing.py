from channels.routing import ProtocolTypeRouter, URLRouter
# import app.routing
from django.urls import re_path
from app.consumers import TextRoomConsumer

# websocket_urlpatterns: This list contains the URL patterns for WebSocket connections. 
# It works similarly to Django’s urlpatterns in urls.py, but specifically for WebSocket connections.
websocket_urlpatterns = [
    re_path(r"ws/(?P<room_name>\w+)/$", TextRoomConsumer.as_asgi()),
]


# ProtocolTypeRouter: This is a router that directs traffic based on the protocol type. 
# For example, it can route HTTP requests, WebSocket connections, and other protocols to the appropriate consumers or views.

# the websocket will open at 127.0.0.1:8000/ws/<room_name>
application = ProtocolTypeRouter({
    'websocket':
        # URLRouter: This is used to route WebSocket connections to the appropriate consumer based on the URL pattern.
        URLRouter(
            websocket_urlpatterns
        )
    ,
})

# re_path(regular expression path) instead of path for urls
# r'^ws/(?P<room_name>[^/]+)/$': The Regular Expression
# r'...': The r before the string indicates a raw string in Python, which means that backslashes (\) are treated literally, rather than as escape characters.

# ^ws/: The ^ symbol signifies the start of the URL. The pattern expects the URL to start with ws/.

# Example: This matches URLs that begin with ws/, like ws/chatroom1/.
# (?P<room_name>[^/]+):

# This is a named capturing group in regex.
# (?P<room_name>...): This syntax captures part of the URL and names it room_name. The captured part can then be accessed in your code.
# [^/]+: This part of the regex means "match one or more characters that are not a /". Essentially, it captures everything between ws/ and the next / or the end of the string.
# Example: In the URL ws/chatroom1/, the regex captures chatroom1 and assigns it to the room_name variable.
# /$: The $ symbol signifies the end of the URL. This ensures that the pattern only matches URLs that end right after the room_name (followed by a /).