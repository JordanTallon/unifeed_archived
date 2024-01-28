from django.shortcuts import render, redirect
from .models import Folder
from .forms import FolderForm

def folder_list(request):
    folders = Folder.objects.all()
    return render(request, 'folder_system/folder_list.html', {'folders': folders})

def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('folder_list')
    else:
        form = FolderForm()

    return render(request, 'folder_system/create_folder.html', {'form': form})
