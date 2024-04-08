import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, seed_url):
        self.seed_url = seed_url
        self.visited_url = set()
        self.url_to_visit = []

    def crawl(self, url):
        self.url_to_visit.append(url)
        while len(self.url_to_visit) > 0:
            current_url = self.url_to_visit.pop(0)
            if current_url not in self.visited_url:

                try:
                    response = requests.get(current_url)
                    html_content = response.content
                    soup = BeautifulSoup(html_content, "html.parser")
                    sub_links = self.extract_all_hyperlinks_in_page(current_url, soup)
                    self.url_to_visit += sub_links

                except Exception as e:
                    print(f"Error fetching url: {url}")
                    print(str(e))


    def get_absolute_url(self, base_url: str, current_url: str):
        if current_url.startswith("https"):
            return current_url
        else:
            return base_url + current_url

    def get_domain(self, url):
        return url.split("://")[1].split("/")[0]

    def extract_all_hyperlinks_in_page(self, base_url: str, soup: BeautifulSoup):
        links = soup.select("a")
        urls = []
        for link in links:
            url = self.get_absolute_url(base_url, link["href"])

            if url not in self.visited_url:
                urls.append(url)

        return urls
