import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Crawler:
    def __init__(self, max_pages, urls=[]):
        self.max_pages = max_pages = max_pages
        self.urls_to_visit = urls
        self.urls_visited = []
        
    # This function will check if the URL is valid and return the HTML content of the page if so (get a 200 status code)
    def valid_url(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            return soup
        else:
            print(f"Error: {r.status_code}")
            return None
    
    # This function will return the domain name of the URL
    def get_domain_name(self, url):
        domain = re.search(r"w?[a-v|x-z][\w%\+-\.]+\.(org|fr|com|net)", url)
        domain_site = domain.group()
        return domain_site
        
    # This function will get all the internal URLs of the page
    def get_internal_urls(self, url):
        html = self.valid_url(url)
        domain_site = self.get_domain_name(url)
        
        for link in html.find_all('a'):
            if 'href' in link.attrs:
                if domain_site in link.attrs['href']:
                    if ("http" in link.attrs['href']):
                        internal_link = link.attrs['href']
                        self.add_url_to_visit(internal_link)
                else:
                    if link.attrs['href'].startswith('/'):
                        internal_link = urljoin(url, link.attrs['href'])
                        if domain_site in internal_link:
                            self.add_url_to_visit(internal_link)
              
    # This function will add the internal URLs to the list of URLs to visit              
    def add_url_to_visit(self, internal_links):
        if internal_links not in self.urls_to_visit and internal_links not in self.urls_visited:
            self.urls_to_visit.append(internal_links)
    
    # This function will run the crawler
    def run(self):
        while self.urls_to_visit and len(self.urls_visited) < self.max_pages:
            url = self.urls_to_visit[0]
            print(f"Crawling: {url}")
            try:
                self.get_internal_urls(url)
                self.urls_visited.append(url)
            except AttributeError:
                print("Error: Not crawlable")
            finally:
                self.urls_to_visit.pop(0)
            # print(self.urls_to_visit)
            # print(self.urls_visited)
            print(f"Crawled {len(self.urls_visited)}")
            

def main():
    url = str(input("Enter the URL: "))
    Crawler(max_pages=2000, urls=[url]).run()
    # Crawler(max_pages=900, urls=["https://www.decathlon.fr/"]).run()
    

if __name__ == "__main__":
    main()