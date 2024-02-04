from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

# This page can only be viewed by the current logged in user
# Therefore, we can just get the current authenticated user and not worry about passing information to the view
User = get_user_model()


class UserProfileForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    track_analytics = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # TODO initialize fields

    def save(self, user=None):
        # TODO handle saving
        pass
