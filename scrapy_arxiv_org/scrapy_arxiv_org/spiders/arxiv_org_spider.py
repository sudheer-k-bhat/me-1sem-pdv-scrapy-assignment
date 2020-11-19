import scrapy 
from scrapy.http import Request

from ..items import ScrapyArxivOrgItem

class firstSpider(scrapy.Spider): 
  name = "basic"
  start_urls = [ 
    "https://arxiv.org/list/eess.IV/recent"
   ]

  def parse(self, response):
    item = ScrapyArxivOrgItem()

    papers = response.css('dd')
    links = response.css('dt')

    for paper, link in zip(papers, links):
      title = paper.css('div.meta div.list-title.mathjax::text').extract()[1].replace('\n' , '')
      lnk = link.css('span.list-identifier a[title="Abstract"]::attr(href)').extract()
      item['title'] = title
      item['link'] = f"https://arxiv.org{lnk[0]}"
      request = Request(item['link'],callback=self.parse_abstract, meta={'item':item})
      yield request
  
  def parse_abstract(self, response):
    item = response.meta["item"]
    item['abstract'] = ''.join(response.css('blockquote.abstract.mathjax::text').extract()).replace('\n', '')
    yield item