from django.urls import path
from . import views

urlpatterns = [
    path('folder/add', views.add_new_folder, name='add_new_folder'),
    path('folder/delete/<int:folder_id>/',
         views.delete_folder, name='delete_folder'),
    path('folder/edit/<int:folder_id>/',
         views.edit_existing_folder, name='edit_existing_folder'),
    # path('api/import/feed', views.import_new_feed, name='import_new_feed'),
    path('<str:folder_name>/add_feed',
         views.add_user_feed_to_folder, name='add_user_feed_to_folder'),
    path('<int:user_id>/<int:folder_id>/',
         views.view_userfeed, name='view_userfeed'),
    path('<int:user_id>/<int:folder_id>/<int:userfeed_id>/',
         views.view_userfeed, name='view_userfeed'),

]
