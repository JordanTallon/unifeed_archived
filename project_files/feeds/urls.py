from django.urls import path
from . import views

urlpatterns = [
    path('folders/', views.folder_list, name='folder_list'),
    path('folders/create/', views.create_folder, name='create_folder'),
]
