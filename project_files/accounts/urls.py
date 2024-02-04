from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.account_register, name="register"),
    path('login/', views.account_login, name="login"),
    path('logout/', views.account_logout, name="logout")
]
