from django.urls import path
from . import views

urlpatterns = [
    path('add/folder', views.add_new_folder, name='add_new_folder'),
    # path('api/import/feed', views.import_new_feed, name='import_new_feed'),
    # path('api/import/user_feed', views.import_user_feed, name='import_new_feed'),
    path('<int:user_id>/<int:folder_id>/',
         views.view_userfeed, name='view_userfeed'),
    path('<int:user_id>/<int:folder_id>/<int:userfeed_id>/',
         views.view_userfeed, name='view_userfeed'),

]
