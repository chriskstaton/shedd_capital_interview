from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_observations),
    path('create/', views.create_observation),
]
