from django.urls import path
from . import views

urlpatterns = [
    path('folder/add', views.add_new_folder, name='add_new_folder'),
    path('folder/delete/<int:folder_id>/',
         views.delete_folder, name='delete_folder'),
    path('folder/edit/<int:folder_id>/',
         views.edit_folder, name='edit_folder'),
    # path('api/import/feed', views.import_new_feed, name='import_new_feed'),
    path('userfeed/add/<str:folder_name>',
         views.add_user_feed_to_folder, name='add_user_feed_to_folder'),
    path('userfeed/delete/<int:userfeed_id>',
         views.delete_userfeed, name='delete_userfeed'),
    path('userfeed/edit/<int:userfeed_id>',
         views.edit_userfeed, name='edit_userfeed'),
    path('<int:user_id>/<int:folder_id>/',
         views.view_userfeed, name='view_userfeed'),
    path('<int:user_id>/<int:folder_id>/<int:userfeed_id>/',
         views.view_userfeed, name='view_userfeed'),

]
