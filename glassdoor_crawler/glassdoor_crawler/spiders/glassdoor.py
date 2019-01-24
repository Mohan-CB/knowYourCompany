# -*- coding: utf-8 -*-
import scrapy
import pdb
import uuid

class GlassdoorSpider(scrapy.Spider):
    name = 'glassdoor'
    # allowed_domains = ['https://www.glassdoor.com']
    # start_urls = ['https://www.glassdoor.com/Reviews/Ascension-Reviews-E1036988.htm']

    # scrapy runspider spiders/glassdoor.py -a start_url=https://www.glassdoor.cotempm/Reviews/Ascension-Reviews-E1036988.htm
    def __init__(self, *args, **kwargs): 
      super().__init__(*args, **kwargs)
      self.start_urls = [kwargs.get('start_url')] 

    def parse(self, response):
        companyName = response.url.split('/')[-1].split('-')[0]
        reviewFeedsList = response.css("#ReviewsFeed").xpath('ol/li')

        for item in reviewFeedsList:
            # pdb.set_trace()
            time = self.parseHelper(item, 'div/div[1]/div/time/text()')
            title = self.parseHelper(item, 'div/div[2]/div/div[2]/h2/a/span/text()')
            starRating = self.parseHelper(item.css('.rating'), 'span/@title')
            job = self.parseHelper(item, 'div/div[2]/div/div[2]/div/div[2]/div/span[1]/span/text()')
            summary = self.parseHelper(item, 'div/div[3]/div/div[2]/p/text()')
            pros = self.parseHelper(item, 'div/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/p[2]/text()')
            cons = self.parseHelper(item, 'div/div[3]/div/div[2]/div[2]/div[1]/div[2]/div/p[exi2]/text()')
            uid = uuid.uuid5(uuid.NAMESPACE_X500, title)
            # save in database
        pass  

    def parseHelper(self, item, xPath):
        temp = item.xpath(xPath)
        if temp != None:
            temp = temp.extract()
            if len(temp) == 0:
                return ''
            else: 
                return temp[0].strip()
        else:
            return ''
