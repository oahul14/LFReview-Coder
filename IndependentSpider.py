#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 21:56:30 2019

@author: luhao
"""

import scrapy
from Indeed_jobsite.items import UniversalSpiderItem


class IndependentSpider(scrapy.Spider):
    name = "IndependentSpider"
    allowed_domains = ['independentjobs.independent.co.uk']
    start_urls = ["https://independentjobs.independent.co.uk/searchjobs/?keywords=landfill&countrycode=GB&Page=1", 
                  "https://independentjobs.independent.co.uk/searchjobs/?keywords=landfill&countrycode=GB&Page=2", 
                  "https://independentjobs.independent.co.uk/searchjobs/?keywords=landfill&countrycode=GB&Page=3"]

    def parse(self, response): 
        hrefs = response.xpath("//h3['lister__header']/a/@href").extract()
        for href in hrefs:
            href = 'https://independentjobs.independent.co.uk' + href[4:-8]
            yield scrapy.Request(href, callback=self.parse_dir_contents, dont_filter=True)	
			
            
    def parse_dir_contents(self, response):
        item = UniversalSpiderItem()
        item['jobinfo'] = ' '.join(response.xpath("//div[@class='grid-item four-fifths lap-one-whole  palm-one-whole']/h1/text()").extract())
        item['company'] = ' '.join(response.xpath("//div[@class='block--larger card highlight-lighter']/dl/div[1]/dd/span/text()").extract())
        item['location'] = ' '.join(response.xpath("//div[@class='block--larger card highlight-lighter']/dl/div[2]/dd/span/text()").extract())
        item['postcode'] = 'Not available'
        item['description'] = ' '.join(response.xpath("string(//div[@class='block fix-text job-description'])").extract())[7:-6]

        yield item