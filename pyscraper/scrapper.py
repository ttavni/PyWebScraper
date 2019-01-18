from bs4 import BeautifulSoup
import re
import urllib.request


def ExtractSoup(url):
	""" Scrapes urls for BS4 soup """

	url = re.sub(r'\s+', '', url)
	req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	page = urllib.request.urlopen(req)
	soup = BeautifulSoup(page, "html.parser")
	return soup


def ExtractMeta(soup):
	"""Takes in a soup from BS4 and produces a dictionary containing all meta tags on a page"""

	meta_tags = []
	meta_values = []
	meta_names = ['property', 'name', 'http-equiv', 'charset']

	for i in range(len(soup.find_all("meta"))):
		for idx in meta_names:
			try:
				meta_tags.append(soup.find_all("meta")[i][idx])
			except:
				pass

	for tag in meta_tags:
		for idx in meta_names:
			try:
				desc = soup.findAll(attrs={idx: re.compile(tag, re.I)})
				meta_values.append(desc[0]['content'].encode('utf-8'))

			except:
				pass

	meta_dict = dict(zip(meta_tags, meta_values))

	return meta_dict


def SoupExtraction(url):
	""" Collect features from URLs"""

	# Create soup
	soup = ExtractSoup(url)

	# Extract all features
	url_dict = {'URL': url,
				'title': soup.find('title').string,
				'h1_text': "".join([element.text for element in soup.findAll('h1')]),
				'p_text': "".join([element.text for element in soup.findAll('p')]),
				'hrefs': [link.get('href') for link in soup.findAll('a')],
				'img_links': soup.findAll('img'),
				'iframes': soup.find_all('iframe'),
				'videos': soup.find_all('video'),
				'meta': ExtractMeta(soup),
				'HTML': soup}

	return url_dict

def BatchScrape(page_urls):

	completed_urls, broken_urls = [], []

	for url in page_urls:
		try:
			url_dict = SoupExtraction(url)
			completed_urls.append(url_dict)
		except:
			broken_urls.append(url)

	return completed_urls, broken_urls