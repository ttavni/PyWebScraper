# Web Scraping for Python
A set of functions and classes to help web scraping and simple web audits

```python
from pyscraper.sitemapper import Sitemapper
from pyscraper.scrapper import BatchScrape

sitemap = 'https://www.datascience.com/sitemap.xml'

page_urls = Sitemapper(sitemap)
completed_urls, broken_urls = BatchScrape(page_urls)
```
# In addition you can now visualise the hierachical nature of the sitemap and produce a d3.js visualisation

```python
# Visualise pages
from pyscraper.viz import VisualiseSitemap
VisualiseSitemap(page_urls)
```

![Visualisation](https://i.imgur.com/roapOsx.png)

The text from each page could then be visualised using this [repository](https://github.com/tavni96/2D_Text_Clustering)