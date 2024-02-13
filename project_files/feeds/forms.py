from .models import FeedFolder
from django.forms import ModelForm


class FeedFolderForm(ModelForm):
    class Meta:
        model = FeedFolder
        fields = ["name"]
