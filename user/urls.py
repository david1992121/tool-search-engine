"""
API URLs for User
"""

from django.urls import path, include
from .views import *

urlpatterns = [
    path("", get_users, name="user-list"),
    path('login', login, name="user-login"),
    path('register', register, name="user-register"),
    path('info', info, name="user-info"),
    path('profile/image', add_avatar, name="user-add-avatar"),
    path('profile/name', change_name, name="user-change-name")
]
