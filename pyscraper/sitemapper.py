from pyscraper.scrapper import ExtractSoup

def Sitemapper(sitemap):
	# Find other sitemaps or pages
	soup = ExtractSoup(url=sitemap)
	urls = [element.text for element in soup.findAll('loc')]
	sitemap_urls = [x for x in urls if '.xml' in x or 'robotsitemap' in x]
	page_urls = list(set(urls) - set(sitemap_urls))

	# Extract all nested sitemaps
	completed_sitemaps = []
	while len(sitemap_urls) > 0:
		for url in sitemap_urls:
			soup = ExtractSoup(url)
			links = [element.text for element in soup.findAll('loc')]
			sitemap_urls += [x for x in links if '.xml' in x or 'robotsitemap' in x]
			page_urls += list(set(links) - set(sitemap_urls))
			sitemap_urls = [x for x in sitemap_urls if x not in completed_sitemaps]
			completed_sitemaps.append(url)

	return list(set(page_urls))