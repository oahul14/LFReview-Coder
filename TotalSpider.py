#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 23:54:27 2019

@author: luhao
"""

import scrapy
from Indeed_jobsite.items import UniversalSpiderItem
import re


class TotalSpider(scrapy.Spider):
    name = "TotalSpider"
    allowed_domains = ['totaljobs.com']
    start_urls = ["https://www.totaljobs.com/jobs/landfill", 
                  "https://www.totaljobs.com/jobs/landfill?page=2", 
                  "https://www.totaljobs.com/jobs/landfill?page=3",
                  "https://www.totaljobs.com/jobs/landfill?page=4", 
                  "https://www.totaljobs.com/jobs/landfill?page=5", 
                  "https://www.totaljobs.com/jobs/landfill?page=6"]

    def parse(self, response): 
        hrefs = response.xpath("//div[@class='col-xs-12 job-results clearfix']/div[starts-with(@class, 'job')]/div/div/div[1]/a/@href").extract()
        for href in hrefs:
            yield scrapy.Request(href, callback=self.parse_dir_contents, dont_filter=True)	
			
            
    def parse_dir_contents(self, response):
        item = UniversalSpiderItem()
        item['jobinfo'] = ' '.join(response.xpath("//h1[@class='brand-font']/text()").extract()).replace('\n','').replace(' ', '').replace('\r', '').replace('\t', '')
        item['company'] = ' '.join(response.xpath("//li[@class='company icon']/div/a/text()").extract()).replace('\n','').replace(' ', '').replace('\r', '').replace('\t', '')
        
        if response.xpath("//li[@class='location icon']").extract() == []:
            item['location'] = ' '.join(response.xpath("//div[@class='col-xs-12 col-sm-7 travelTime-locationText']/ul/li/text()").extract()).replace('\n','').replace(' ', '').replace('\r', '').replace('\t', '')
        else: 
            item['location'] = ' '.join(response.xpath("string(//li[@class='location icon'])").extract()).replace('\n','').replace(' ', '').replace('\r', '').replace('\t', '')
        
        item['postcode'] = 'Not Available'
        item['description'] = ' '.join(response.xpath("string(//div[@class='job-description'])").extract())

        yield item