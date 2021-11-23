"""
API URLs for User
"""

from django.urls import path, include
from .views import *

urlpatterns = [
    path("", get_users),
    path('login', login),
    path('register', register),
    path('info', info),
    path('profile/image', add_avatar),
    path('profile/name', change_name)
]
