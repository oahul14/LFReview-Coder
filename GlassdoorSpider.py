#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 10:48:34 2019

@author: luhao
"""

import scrapy
from Indeed_jobsite.items import UniversalSpiderItem



class GlassdoorSpider(scrapy.Spider):
    name = "GlassdoorSpider"
    allowed_domains = ['glassdoor.co.uk']
    start_urls = ["https://www.glassdoor.co.uk/Job/landfill-jobs-SRCH_KO0,8_IP1.htm"]
    npages = list(range(2, 12))
    for i in npages:
        start_urls.append("https://www.glassdoor.co.uk/Job/landfill-jobs-SRCH_KO0,8_IP"+str(i)+".htm")

    def parse(self, response): 
        hrefs = response.xpath("//*[@id='MainCol']/div/ul/li[@class='jl selected']/div[2]/div[1]/div[1]/a/@href").extract() + response.xpath("//*[@id='MainCol']/div/ul/li[@class='jl']/div[1]/a/@href").extract()
        for href in hrefs:
            href = "https://www.glassdoor.co.uk" + href
            yield scrapy.Request(href, callback=self.parse_dir_contents, dont_filter=True)	
			
            
    def parse_dir_contents(self, response):
        item = UniversalSpiderItem()
        item['jobinfo'] = ' '.join(response.xpath("//div[@class='jobViewJobTitleWrap']/h2/text()").extract())
        item['company'] = ' '.join(response.xpath("//span[@class='strong ib']/text()").extract())
        item['location'] = ' '.join(response.xpath("//span[@class='subtle ib']/text()").extract())[3:]
        item['postcode'] = 'Not available'
        item['description'] = ' '.join(response.xpath("string(//div[@id='JobDescriptionContainer']/div/div)").extract())

        yield item
