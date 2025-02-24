from django.urls import path
from . import views

urlpatterns = [
    path('', views.validate_file, name='validate_file'),
    path('', views.validate_file, name='upload_file'),
]