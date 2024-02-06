from django.urls import path
from . import views

urlpatterns = [
    path('import', views.import_new_feed, name='import_new_feed')
]
