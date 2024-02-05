# rss_app/forms.py
from django import forms
from folder_system.models import Folder

class FeedForm(forms.Form):
    rss_url = forms.URLField(label='RSS Feed URL')
    folder = forms.ModelChoiceField(queryset=Folder.objects.all(), label='Select a Folder')

    def __init__(self, *args, **kwargs):
        folder_id = kwargs.pop('folder_id', None)
        super(FeedForm, self).__init__(*args, **kwargs)

        if folder_id is not None:
            # Adjust the queryset for the folder field based on the provided folder_id
            self.fields['folder'].queryset = Folder.objects.filter(id=folder_id)




