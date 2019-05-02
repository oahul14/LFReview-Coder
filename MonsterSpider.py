#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 14:49:06 2019

@author: luhao
"""

import scrapy
from Indeed_jobsite.items import UniversalSpiderItem
import re


class MonsterSpider(scrapy.Spider):
    name = "MonsterSpider"
    allowed_domains = ['monster.co.uk']
    start_urls = ["https://www.monster.co.uk/jobs/search/?q=landfill&where=&intcid=swoop_Hero_Search&cy=uk&rad=20&client=&stpage=1&page=3"]
        
    def parse(self, response): 
        hrefs = response.xpath("//header[@class='card-header']/h2/a/@href").extract()
        for href in hrefs:
        #    if href.startswith("http") is False:
        #        href = "https://www.monster.co.uk" + href
        #        t=1
        #        time.sleep(t)
            yield scrapy.Request(href, callback=self.parse_dir_contents)	
			
            
    def parse_dir_contents(self, response):
        item = UniversalSpiderItem()
        jobinfo_company = ' '.join(response.xpath("//h1[@class='title']/text()").extract())
        item['jobinfo'] = re.split(' - | found on ', jobinfo_company)[0]
        item['company'] = re.split(' - | found on ', jobinfo_company)[1]
        item['location'] = ' '.join(response.xpath("//h2[@class='subtitle']/text()").extract())
        item['postcode'] = re.split(', ', item['location'])[-1]
        item['description'] = ' '.join(response.xpath("string(//div[@id='JobDescription'])").extract())[4:-12]

        yield item
