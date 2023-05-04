import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class CrawlingSpider():
    name = "crawler"
    allowed_domains = ["toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        soup = BeautifulSoup(response.content, "html.parser")
        categories = soup.select("div.side_categories > ul > li > ul > li > a")
        for category in categories:
            category_link = urljoin(self.start_urls[0], category["href"])
            category_page = requests.get(category_link).content
            category_soup = BeautifulSoup(category_page, "html.parser")
            products = category_soup.select(".product_pod > h3 > a")
            for product in products:
                product_link = urljoin(category_link, product["href"])
                product_page = requests.get(product_link).content
                product_soup = BeautifulSoup(product_page, "html.parser")
                title = product_soup.select(".product_main > h1")[0].text
                price = product_soup.select(".price_color")[0].text
                availability = product_soup.select(".availability")[0].text.strip().replace("\n", "")
                img = product_soup.select(".active > img")[0]["src"]
                item = {
                    "title": title,
                    "price": price,
                    "availability": availability,
                    "img": img
                }
                print(item)
                with open("output_bs4.json", "a") as f:
                    f.write(json.dumps(item) + "\n")


CrawlingSpider().parse(requests.get("http://books.toscrape.com/"))
