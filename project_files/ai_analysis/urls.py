from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyse_article_bias, name="analyse_article_bias"),
    path('feedback/', views.provide_analysis_feedback,
         name="provide_analysis_feedback"),
    path('check/<int:analysis_id>/', views.check_analysis_status,
         name='check_analysis_status'),
]
