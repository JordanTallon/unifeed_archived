# rss_app/forms.py
from django import forms
from folder_system.models import Folder

class FeedForm(forms.Form):
    rss_url = forms.URLField(label='RSS Feed URL')
    folder = forms.ModelChoiceField(queryset=Folder.objects.all(), required=False, label='Folder')

