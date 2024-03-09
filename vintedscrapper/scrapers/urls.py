from django.urls import path
from .views import scrape_hacker_news

urlpatterns = [
    path("scrape-hacker-news/", scrape_hacker_news, name="scrape_hacker_news"),
]