from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyse_article_bias, name="analyse_article_bias"),
    path('check/<int:analysis_id>/', views.check_analysis_status,
         name='check_analysis_status'),
]
