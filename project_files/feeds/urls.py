from django.urls import path
from . import views

urlpatterns = [
    path('import', views.importFeed, name='import_feed')
]
