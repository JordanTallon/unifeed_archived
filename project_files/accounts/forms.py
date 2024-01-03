from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'track_analytics']


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']
