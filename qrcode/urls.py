"""
API URLs for QrCode
"""

from django.urls import path, include
from .views import *

urlpatterns = [
    path('item', get_item_code, name="item-code"),
]
