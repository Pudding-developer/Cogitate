from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Custom user model with additional fields
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    # Avatar field with default value
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    # Model representing discussion topics
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    # Model representing discussion rooms
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    # Model representing messages in a room
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]


class Event(models.Model):
    # Model representing events/tasks
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "tblevents"  # Custom database table name
