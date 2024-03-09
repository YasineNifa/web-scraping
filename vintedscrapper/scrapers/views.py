from django.shortcuts import render
from django.http import JsonResponse

import scrapy
from scrapy.crawler import CrawlerProcess
# from scrapers.spiders.hacker_news_spider import HackerNewsSpider
# Create your views here.

class HackerNewsSpider(scrapy.Spider):
    name = "hacker_news"
    start_urls = [
        "https://news.ycombinator.com/"
    ]
    def parse(self, response):
        for article in response.css("tr.athing"):
            yield {
                "title": article.css("span.titleline::text").get(),
                # "votes": int(article.css("span.score::text").re_first(r"\d+"))
            }
        next_page = response.css("a.morelink::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


def scrape_hacker_news(request):
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    })
    process.crawl(HackerNewsSpider)
    process.start(stop_after_crawl=False)
    with open("items.json", "r") as f:
        data = f.read()
    return JsonResponse(data, safe=False)