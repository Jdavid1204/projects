from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class PageView(models.Model):
    """
    Model to track the number of page views.

    Attributes:
        count (int): The count of page views.
    """
    count: models.IntegerField = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Page view count: {self.count}"


class Hobby(models.Model):
    """
    Model to represent a hobby.

    Attributes:
        name (str): The name of the hobby.
        description (str): A description of the hobby (optional).
    """
    name: models.CharField = models.CharField(max_length=255, unique=True)
    description: models.TextField = models.TextField(blank=True)

    def save(self, *args, **kwargs) -> None:
        """
        Overrides the save method to clean and capitalize the hobby name.
        """
        if self.name:
            self.name = self.name.strip().capitalize()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class FriendRequest(models.Model):
    """
    Model to represent a friend request between users.

    Attributes:
        sender (CustomUser): The user who sent the friend request.
        receiver (CustomUser): The user who received the friend request.
        status (str): The status of the friend request (pending, accepted, or declined).
        timestamp (datetime): The time when the friend request was created.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_friend_requests",
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_friend_requests",
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('declined', 'Declined'),
        ],
        default='pending',
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django AbstractUser.

    Attributes:
        email (str): The user's email address.
        date_of_birth (date): The user's date of birth.
        hobbies (ManyToManyField): The hobbies associated with the user.
        friends (ManyToManyField): The user's friends.
    """
    email: models.EmailField = models.EmailField(unique=True)
    date_of_birth: models.DateField = models.DateField()
    hobbies: models.ManyToManyField = models.ManyToManyField(Hobby, blank=True)

    friends = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'date_of_birth']

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"
