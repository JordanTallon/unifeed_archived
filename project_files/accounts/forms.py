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
        widget=forms.PasswordInput,
        required=False
    )

    password2 = forms.CharField(
        label='New password confirmation',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    # https://docs.djangoproject.com/en/5.0/ref/forms/validation/
    # (for reminder on clean, TLDR: django automatically runs the clean function during form validation)
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # If both passwords were provided
        if password1 and password2:
            # If they don't match, raise an error
            if password1 != password2:
                raise ValidationError(
                    {'password2': ["Passwords don't match."]})

            # Both passwords exist and match, check if they are secure/valid
            # https://docs.djangoproject.com/en/5.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
            try:
                password_validation.validate_password(password1, self.instance)
            except ValidationError as errors:
                # If the password isn't valid, raise an error
                raise ValidationError({'password1': errors})

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user
