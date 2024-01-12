from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.getData, name="get-political-bias"),
    path('add/', views.postPoliticalBiasAnalysis, name="add-political-bias"),
]
