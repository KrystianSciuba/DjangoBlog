from django.urls import path

from .views import (
    user_page_view)

urlpatterns = [
    path('<str:username>/', user_page_view, name="userpage")
    
    ]