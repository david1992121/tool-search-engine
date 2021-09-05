"""
API URLs for Program
"""

from django.urls import path, include
from .views import *

urlpatterns = [
    path('', get_programs),
    path('tooling', get_toolings),
    path('tools', get_tools),
    path('pdf', download_pdf)
]