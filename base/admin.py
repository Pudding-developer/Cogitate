from django.contrib import admin
from .models import Room, Topic, Message, User, Event

# Register the models with the Django admin site
admin.site.register(User)    # Registering User model
admin.site.register(Room)    # Registering Room model
admin.site.register(Topic)   # Registering Topic model
admin.site.register(Message) # Registering Message model
admin.site.register(Event)   # Registering Event model
