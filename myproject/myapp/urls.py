from django.urls import path
from . import views

urlpatterns = [
    path('fetch_and_extract_menu/', views.fetch_and_extract_menu, name='fetch_and_extract_menu'),
    # Add more URL patterns as needed
]
