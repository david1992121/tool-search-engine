"""
API URLs for User
"""

from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', login),
    path('register', register),
    path('info', info),
]
