import uuid
from django.contrib.auth import get_user_model


def create_custom_user(email, username, first_name, last_name, date_of_birth, password="User12345"):
    """
    Helper function to create a custom user.
    """
    custom_user = get_user_model()
    try:
        return custom_user.objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
    except Exception as e:
        raise RuntimeError(f"Error creating user {username}: {e}")

def create_user(password="User12345"):
    unique_id = str(uuid.uuid4())[:8]
    return create_custom_user(
        email=f"testuser{unique_id}@example.com",
        username=f"testuser{unique_id}",
        first_name="Test",
        last_name="User",
        date_of_birth="2000-01-01",
        password=password,
    )

def create_sender_receiver(password="User12345"):
    """
    Helper method to create unique sender and receiver test users.
    """
    unique_id = str(uuid.uuid4())[:8]
    sender = create_custom_user(
        email=f"sender{unique_id}@example.com",
        username=f"senderUser{unique_id}",
        first_name="Sender",
        last_name="User",
        date_of_birth="2000-12-12",
        password=password,
    )
    receiver = create_custom_user(
        email=f"receiver{unique_id}@example.com",
        username=f"receiverUser{unique_id}",
        first_name="Receiver",
        last_name="User",
        date_of_birth="2000-01-01",
        password=password,
    )
    return sender, receiver
