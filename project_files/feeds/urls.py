from django.urls import path
from . import views

urlpatterns = [
    path('api/import/feed', views.import_new_feed, name='import_new_feed'),
    path('api/import/user_feed', views.import_user_feed, name='import_new_feed'),
    path('<int:user_id>/<int:folder_id>',
         views.view_folder, name='view_folder'),
    path('<int:user_id>/<int:folder_id>/<int:userfeed_id>',
         views.view_userfeed, name='view_userfeed'),
]
