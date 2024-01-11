from django.urls import path
from .views import user_profile, user_profile_update

urlpatterns = [
    path('profile/', user_profile, name='profile'),
    path('profile/edit/', user_profile_update, name='edit_profile'),
]
