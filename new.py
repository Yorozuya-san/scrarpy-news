# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.loader import ItemLoader
from news.items import NewsItem
 
class NewSpider(scrapy.Spider):
    name = 'new'
    #allowed_domains = ['https://news.google.com/news/?ned=in']
    start_urls = ['http://www.thehindu.com/','https://timesofindia.indiatimes.com/']

    def parse(self, response):
        global start_urls
        self.l = ItemLoader(item=NewsItem() , response=response)
        print(self.start_urls[0])
       # yield scrapy.Request(url=self.start_urls[0],callback=self.thehindumain)
        self.l = ItemLoader(item=NewsItem() , response=response)
       # yield scrapy.Request(url=self.start_urls[1],callback=self.thetimesmain)
        #self.l = ItemLoader(item=NewsItem() , response=response)
        while True:
            self.l = ItemLoader(item=NewsItem() , response=response)
            #buiss
        #    yield scrapy.Request(url='http://www.thehindu.com/business/',callback=self.thehindumain)
         #   yield scrapy.Request(url='https://timesofindia.indiatimes.com/business' , callback=self.thetimestopic)
            #interna
            yield scrapy.Request(url='http://www.thehindu.com/news/international/',callback=self.thehindumain)
            yield scrapy.Request(url='https://timesofindia.indiatimes.com/world/', callback=self.thetimestopic)
            #india
            #yield scrapy.Request(url='http://www.thehindu.com/news/national/',callback=self.thehindumain)
            #yield scrapy.Request(url='https://timesofindia.indiatimes.com/india',callback=self.thetimestopic)
            #sports
            #yield scrapy.Request(url='http://www.thehindu.com/news/sport/',callback=self.thehindumain)
            #yield scrapy.Request(url='https://timesofindia.indiatimes.com/sports',callback=self.thetimestopic)
            #tech
           # yield scrapy.Request(url='http://www.thehindu.com/news/technology/',callback=self.thehindumain)
           # yield scrapy.Request(url='https://www.gadgetsnow.com?utm_source=toiweb&utm_medium=referral&utm_campaign=toiweb_hptopnav',callback=self.thetimestopic)
            #sci
            #yield scrapy.Request(url='http://www.thehindu.com/news/sci-tech/',callback=self.thehindumain)
            break
    
    def thehindumain(self,response):
        for i in response.css('div.story-card'):
            t = i.css('a::text').extract()
            for text in t:
                if text.count(' ')<3:#if story or not
                    continue
                if text.count(' ')>=3:
                    head=""
                    self.l.add_value('story', text)
                    self.l.add_value('link',i.css('a::attr(href)').extract_first())
                    self.l.add_value('head', head)
       # yield self.l.load_item()
                    		#yield scrapy.Request(url=li['link'],callback=self.thehindutopic)
    #the hindu article func
    def thehindutopic(self,response):
        	#u=response.url()
        t=response.css('div.article-topics-container')
       	intro = response.css('h2.intro').extract_first()
       	body = response.css('p').extract()
       	yield {
           		'intro' : intro,
           		'body' : body,
        	}

    def thetimesmain(self,response):
        st=[response.css('div.top-story li > a')]#,response.css('div#lateststories li > a')]
        for i in st:
            t = i.css('a::text').extract()
            lin = i.css('a::attr(href)').extract()
            j=0
            for text in t:
                if text.count(' ')<3:
                    continue
                #print('=================here================',text)
                head=""
                self.l.add_value('story',text)
                while True:
                    #print(j,len(lin))
                    if j+1<len(lin):
                        print(j,len(lin))
                        if ("video" in lin[j] or "//photogallery" in lin[j] or lin[j] in lin[j+1:]):
                            j+=1
                        else:
                            break
                    else:
                        break
                if j==len(lin):
                    break
                self.l.add_value('link',response.urljoin(lin[j]))
                self.l.add_value('head',head)
                j+=1
        return self.l.load_item()

    def thetimestopic(self,response):
        t = response.css('span.w_tle a::text').extract()
        l = response.css('span.w_tle a::attr(href)').extract()
        for i in range(len(t)):
            if "video" in l[i] or "photo" in l[i]:
                continue
            self.l.add_value('story',t[i])
            self.l.add_value('link',response.urljoin(l[i]))
        return self.l.load_item()
