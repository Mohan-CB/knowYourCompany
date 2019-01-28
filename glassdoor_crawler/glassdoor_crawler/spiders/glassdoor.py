# -*- coding: utf-8 -*-
import scrapy
import pdb
import uuid
from glassdoor_crawler.items import Review
import redis

class GlassdoorSpider(scrapy.Spider):
    name = 'glassdoor'
    # allowed_domains = ['https://www.glassdoor.com']
    # start_urls = ['https://www.glassdoor.com/Reviews/Ascension-Reviews-E1036988.htm']
    # scrapy runspider spiders/glassdoor.py -a start_url=https://www.glassdoor.com/Reviews/Ascension-Reviews-E1036988.htm
#     scrapy runspider spiders/glassdoor.py -a start_url=https://www.glassdoor.com/Reviews/company-reviews.htm\?suggestCount\=0\&suggestChosen\=false\&clickSource\=searchBtn\&typedKeyword\=Kforce\&sc.keyword\=Kforce\&locT\=\&locId\=\&jobType\=

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.redisClient = redis.StrictRedis(host='localhost',port=6379,db=0)
      self.target = [kwargs.get('target')]
      self.start_urls = [kwargs.get('start_url')]
      
    def parse(self, response):

        if response.url != 'https://www.glassdoor.com/Reviews/index.htm':
            if 'Overview' not in response.url:
                overviewUrl = response.css('#MainCol').xpath('div[1]/div[2]/div[1]/div[1]/a/@href').extract()[0].strip()        
                temp = overviewUrl.split('/')[-1]
                companyName, companyId = temp[11:].split('.')[0].split('-')
                companyId = companyId[4:]
                reviewUrl = 'https://www.glassdoor.com/Reviews/'+ companyName + '-Reviews-' + companyId + '.htm'
            else:
                reviewUrl = 'https://www.glassdoor.com' + response.css('#EIProductHeaders').xpath('div/a[2]/@href').extract()[0].strip()

            # TODO: scrap following pages
            yield scrapy.Request(reviewUrl, callback=self.parseReviewPage,dont_filter=True)

    def parseReviewPage(self, response):
        companyName = self.parseHelper(response.css('.h1'), 'text()')
        if self.redisClient.hget('knowYourCompany', self.target[0]) == None:
            print('save in redis')
            self.redisClient.hset('knowYourCompany',self.target[0], companyName)
        reviewFeedsList = response.css("#ReviewsFeed").xpath('ol/li')

        for item in reviewFeedsList:
            time = self.parseHelper(item, 'div/div[1]/div/time/text()')
            title = self.parseHelper(item, 'div/div[2]/div/div[2]/h2/a/span/text()')
            starRating = self.parseHelper(item.css('.rating'), 'span/@title')
            job = self.parseHelper(item, 'div/div[2]/div/div[2]/div/div[2]/div/span[1]/span/text()')
            summary = self.parseHelper(item, 'div/div[3]/div/div[2]/p/text()')
            pros = self.parseHelper(item, 'div/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/p[2]/text()')
            cons = self.parseHelper(item, 'div/div[3]/div/div[2]/div[2]/div[1]/div[2]/div/p[2]/text()')
            uid = str(uuid.uuid5(uuid.NAMESPACE_X500, title))

            review = Review(time=time,
                            title=title,
                            companyName=companyName,
                            starRating=starRating,
                            job=job,
                            summary=summary,
                            pros=pros,
                            cons=cons,
                            uid=uid)
            yield review
        pass  

    def parseHelper(self, item, xPath):
        temp = item.xpath(xPath)
        if temp != None:
            temp = temp.extract()
            if len(temp) == 0:
                return ''
            else: 
                return temp[0].strip().strip('"')
        else:
            return ''
