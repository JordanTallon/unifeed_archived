from . import views
from django.urls import path

urlpatterns = [
    path('registration/', views.registration, name="registration")
]
