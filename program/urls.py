"""
API URLs for Program
"""

from django.urls import path, include
from .views import *

urlpatterns = [
    path('search', get_programs),
    path('tooling', get_toolings),
    path('tools', get_tools),
    path('pdf', download_pdf),
    path('check', save_check_history),
    path('check/detail', save_check_detail),
    path('history', get_check_histories),
    path('history/detail/<int:id>', get_check_history),
    path('history/details', get_check_detail)
]