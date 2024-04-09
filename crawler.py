import requests
import logging
from bs4 import BeautifulSoup
import time
from collections import deque
from urllib.parse import urlparse


class Crawler:
    def __init__(self, seed_url):
        self.seed_url: str = seed_url
        self.CRAWL_DELAY = 0
        self.MAX_REQUEST_PER_MINUTE: int = 10
        self.visited_url: set = set()
        self.url_to_visit: deque = deque()
        self.domain_limit: dict = {}

        # Set logging config
        logging.basicConfig(filename="logs/crawler.log",
            format="%(asctime)s, %(levelname)s, %(funcName)s, %(pathname)s, %(message)s", level=logging.INFO)

    def crawl(self, url):
        self.url_to_visit.append(url)
        while len(self.url_to_visit) > 0:
            current_url = self.url_to_visit.popleft()
            if current_url in self.visited_url:
                continue
            try:
                url_domain = self.get_domain(current_url)

                if self.can_crawl_domain(url_domain):
                    time.sleep(self.CRAWL_DELAY)
                    response = requests.get(current_url)
                    html_content = response.content
                    self.visited_url.add(current_url)
                    soup = BeautifulSoup(html_content, "html.parser")
                    logging.info("Crawled: %s", current_url)

                    # EXTRACT TEXT
                    self.extract_text(soup)
                    self.extract_all_hyperlinks_in_page(current_url, soup)
                else:
                    logging.info("Reached domain limit for %s", url_domain)
                    self.url_to_visit.append(current_url)

            except Exception as e:
                logging.exception("Exception Occured")

    def get_absolute_url(self, base_url: str, current_url: str):
        if current_url.startswith("https"):
            return current_url
        else:
            return base_url + current_url

    def get_domain(self, url):
        return url.split("://")[1].split("/")[0]

    def can_crawl_domain(self, domain):
        if domain in self.domain_limit:
            domain_rate = self.domain_limit[domain]
            if domain_rate[1] + 1 > self.MAX_REQUEST_PER_MINUTE and (time.time() - domain_rate[0]) > 60:
                new_rate_for_domain = (time.time(), 0)
                self.domain_limit[domain] = new_rate_for_domain
                return True
            elif domain_rate[1] + 1 < self.MAX_REQUEST_PER_MINUTE:
                current = self.domain_limit[domain]
                self.domain_limit[domain] = (current[0], current[1] + 1)
                return True
            else:
                return False
        else:
            self.domain_limit[domain] = (time.time(), 0)
            return True

    def extract_all_hyperlinks_in_page(self, base_url: str, soup: BeautifulSoup):
        links = soup.select("a")
        for link in links:
            try:
                url = self.get_absolute_url(base_url, link["href"])

                if url not in self.visited_url:
                    self.url_to_visit.append(url)
            except Exception as e:
                logging.exception("Exception occurred")

    def is_html_url(self, response: requests.Response):
        content_type = response.headers.get("Content-Type")
        return content_type and "text/html" in content_type

    def extract_text(self, soup: BeautifulSoup):
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator=" ", strip=True)
        print(text)
        return text