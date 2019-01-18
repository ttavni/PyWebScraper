# SimpleWebScrapes
A set of functions and classes to help web scraping and simple web audits

```python
from WebScrape import SitemapWebScrape

sitemap = 'https://www.spotify.com/uk/sitemap.xml'
sws = SitemapWebScrape(sitemap)

# Get all pages from sitemap
sws.FindPages()

# See urls in sitemap
sws.page_urls

# Start scraping all URLs
sws.URLScrape()

# Returns dataframe of results
sws.ReturnDataframe()

# See broken URLs
sws.broken_urls
```
# In addition you can now visualise the hierachical nature of the sitemap and produce a d3.js visualisation

```python
# Visualise pages
from WebScrape import SitemapWebScrape, VisualiseSitemap
sitemap = 'https://www.spotify.com/uk/sitemap.xml'
sws = SitemapWebScrape(sitemap)
sws.FindPages()
VisualiseSitemap(sws.page_urls)
```

![Visualisation](https://i.imgur.com/roapOsx.png)
