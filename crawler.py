import requests
import logging 
from bs4 import BeautifulSoup
import time
from collections import deque


class Crawler:
    def __init__(self, seed_url):
        self.seed_url: str = seed_url
        self.CRAWL_DELAY = 0
        self.MAX_REQUEST_PER_MINUTE: int = 10
        self.visited_url: set = set()
        self.url_to_visit: deque = deque()
        self.domain_limit: dict = {}


        # Initialize logging
        logging.basicConfig(format="%(asctime)s, %(levelname)s, %(funcName)s, %(pathname)s, %(message)s", level=logging.INFO)

    def crawl(self, url):
        self.url_to_visit.append(url)
        while len(self.url_to_visit) > 0:
            current_url = self.url_to_visit.popleft()
            if current_url not in self.visited_url:
                try:
                    url_domain = self.get_domain(current_url)

                    if self.can_crawl_domain(url_domain):
                        time.sleep(self.CRAWL_DELAY)
                        response = requests.get(current_url)
                        html_content = response.content
                        self.visited_url.add(current_url)
                        soup = BeautifulSoup(html_content, "html.parser")
                        logging.info("Crawled: %s", current_url)
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
