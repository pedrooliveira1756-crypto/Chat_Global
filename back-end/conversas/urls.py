# conversas/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health),
    path("create_user/", views.create_user),
    path("messages/", views.messages),
]
