from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
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

    def __init__(self, *args, **kwargs):
        super(AccountSettingsForm, self).__init__(*args, **kwargs)
        # Remove the password field that comes with UserChangeForm
        # Custom fields for it are created in this form
        self.fields.pop('password', None)

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

    def check_passwords_match(self, password1, password2):
        # If both passwords were provided
        if password1 and password2:
            # Return the cleaned data if they match, otherwise continue to error
            if password1 == password2:
                return True

        return False

    def check_password_secure(self, password):
        try:
            # Use password_validation to make sure the password is 'secure'
            # https://docs.djangoproject.com/en/5.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
            password_validation.validate_password(password, self.instance)
        except ValidationError as e:
            # If the password fails validation, add the error
            self.add_error('password1', e)
        return password

    # https://docs.djangoproject.com/en/5.0/ref/forms/validation/
    # (for reminder on clean, TLDR: it runs automatically during form validation)
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not self.check_passwords_match(password1, password2):
            # Either the passwords didn't match or one was missing
            self.add_error('password2', "Passwords don't match.")

        password1 = self.check_password_secure(password1)

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user
