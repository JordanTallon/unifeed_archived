from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.postPoliticalBiasAnalysis, name="add-political-bias"),
    path('all', views.getPoliticalBiasAnalysis, name="get-political-bias")
]
