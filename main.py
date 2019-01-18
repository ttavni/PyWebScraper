__author__ = "T.Avni"

from pyscraper.sitemapper import Sitemapper
from pyscraper.scrapper import BatchScrape
from pyscraper.viz import VisualiseSitemap

if __name__ == "__main__":
	# Dependencies
	sitemap = 'https://www.datascience.com/sitemap.xml'

	page_urls = Sitemapper(sitemap)
	completed_urls, broken_urls = BatchScrape(page_urls)

	VisualiseSitemap(page_urls)
