from .models import FeedFolder, UserFeed
from django.forms import ModelForm, ModelChoiceField
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from .models import UserFeed


class UserFeedForm(forms.ModelForm):
    url = forms.URLField(
        required=False, help_text="Enter URL to import a custom feed")

    class Meta:
        model = UserFeed
        fields = ["feed"]

    def __init__(self, *args, **kwargs):
        super(UserFeedForm, self).__init__(*args, **kwargs)

        # Force the url label to render first
        self.fields = {
            'url': self.fields['url'],
            'feed': self.fields['feed'],
        }

        self.fields['feed'].help_text = "OR Select from one of our many existing feeds"

    def clean(self):
        cleaned_data = super().clean()
        feed = cleaned_data.get("feed")
        url = cleaned_data.get("url")

        if not feed and not url:
            raise ValidationError("You must select a feed or provide a URL.")

        if feed and url:
            raise ValidationError(
                "Please select either a feed or provide a URL, not both.")

        return cleaned_data

    def save(self, commit=True):
        user_feed = super(UserFeedForm, self).save(commit=False)

        if commit:
            user_feed.save()

        return user_feed


class EditUserFeedForm(forms.ModelForm):
    class Meta:
        model = UserFeed
        fields = ["name", "description", "folder"]


class FeedFolderForm(ModelForm):
    class Meta:
        model = FeedFolder
        fields = ["name"]
