from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

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

    password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='New password confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    # https://docs.djangoproject.com/en/5.0/ref/forms/validation/ (for reminder on clean, TLDR: it runs automatically during form validation)
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        # If both passwords were provided
        if password1 and password2:
            # Return the cleaned data if they match, otherwise continue to error
            if password1 == password2:
                return cleaned_data

        # Either the passwords didn't match or one was missing
        self.add_error('password2', "Passwords don't match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user
