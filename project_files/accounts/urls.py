from . import views
from django.urls import path

urlpatterns = [
    path('registration/', views.registration, name="registration"),
    path('login/', views.account_login, name="login"),
    path('logout/', views.account_logout, name="logout")
]
