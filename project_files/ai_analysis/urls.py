from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyse_article_bias, name="analyse-political-bias"),
]
