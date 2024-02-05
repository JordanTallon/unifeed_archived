# folder_system/forms.py
from django import forms
from .models import Folder, FeedItem

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['id', 'name']

class RSSFeedForm(forms.ModelForm):
    class Meta:
        model = FeedItem
        fields = ['title', 'link', 'folder']

