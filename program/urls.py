"""
API URLs for Program
"""

from django.urls import path, include
from .views import *

urlpatterns = [
    path('search', get_programs, name = "programs-list"),
    path('tooling', get_toolings, name = "toolings-list"),
    path('tools', get_tools, name = "tools-list"),
    path('pdf', download_pdf, name = "download-pdf"),
    path('check', save_check_history, name = "save-check-history"),
    path('check/detail', save_check_detail, name = "save-check-detail"),
    path('history', get_check_histories, name = "history-list"),
    path('history/detail/<int:id>', get_check_history, name = "history-retrieve"),
    path('history/details', get_check_detail, name = "history-detail-list")
]
