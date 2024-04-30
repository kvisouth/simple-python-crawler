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
	# We need the headers to avoid getting a 403 status code
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
	# The regex pattern will match the domain name of the URL
	def get_domain_name(self, url):
		domain = re.search(r"w?[a-v|x-z][\w%\+-\.]+\.(org|fr|com|net)", url)
		domain_site = domain.group()
		return domain_site
		
	# This function will get all the internal URLs of the page
	# What is does is that it will get all the 'a' tags of the page and check if the 'href' attribute is in the domain name
	# If it is, it will add the URL to the list of URLs to visit
	# If it is not, it will check if the URL starts with a '/' and if it does, it will join the URL with the domain name
	# If the domain name is in the URL, it will add the URL to the list of URLs to visit
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
	# It will get the first URL of the list of URLs to visit
	# It will write the URL to a file
	# It will get the internal URLs of the page
	# It will append the URL to the list of URLs visited
	# It will remove the URL from the list of URLs to visit
	# It will print how many URLs have been crawled
	# Then loops until there are no more URLs to visit or the number of URLs visited is equal to the maximum number of pages
	def run(self):
		while self.urls_to_visit and len(self.urls_visited) < self.max_pages:
			url = self.urls_to_visit[0]
			print(f"Writing: {url}")
			with open("urls.txt", "a") as f:
				f.write(url + "\n")
			try:
				self.get_internal_urls(url)
				self.urls_visited.append(url)
			except AttributeError:
				print("Error: Not crawlable")
			finally:
				self.urls_to_visit.pop(0)

			print(f"Crawled {len(self.urls_visited)}")
   
	# This function will check if the URL is valid
	def	url_check(url):
		if re.match(r"https?://[a-z0-9-]+\.[a-z0-9-]+", url):
			return True
		else:
			return False

def main():
	url = str(input("Enter URL: "))
	if Crawler.url_check(url) == False:
		print("Invalid URL")
		return
	else:
		Crawler(max_pages=2000, urls=[url]).run()
	
if __name__ == "__main__":
	main()