from django.urls import path
from .views_search import search_view

urlpatterns = [
    path("search/", search_view, name="search"),
]
