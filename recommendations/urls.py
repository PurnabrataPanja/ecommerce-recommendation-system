from django.urls import path
from .views import recommend_view, recommend_api

urlpatterns = [
    path("", recommend_view, name="home"),  
    path("recommend/", recommend_view, name="recommend"),
    path("api/recommend/", recommend_api, name="recommend_api"),
]