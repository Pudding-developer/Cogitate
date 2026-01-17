from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


class MyUserCreationForm(UserCreationForm):
    # Custom user creation form based on UserCreationForm
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    # Form for handling Room model data
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']  # Excluding host and participants from form

class UserForm(ModelForm):
    # Form for handling User model data
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']  # Specifying fields to include in the form
