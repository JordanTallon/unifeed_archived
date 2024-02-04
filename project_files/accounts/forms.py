from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model

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


class AccountSettingsForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
