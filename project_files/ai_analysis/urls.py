from django.urls import path
from . import views

urlpatterns = [
    path('', views.postPoliticalBiasAnalysis, name="add-political-bias"),
]
