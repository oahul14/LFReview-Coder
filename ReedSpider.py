#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 10:02:03 2019

@author: luhao
"""

import scrapy
from Indeed_jobsite.items import UniversalSpiderItem



class ReedSpider(scrapy.Spider):
    name = "ReedSpider"
    allowed_domains = ['Reed.co.uk']
    start_urls = ["https://www.reed.co.uk/jobs/landfill-jobs", "https://www.reed.co.uk/jobs/landfill-jobs?pageno=2", "https://www.reed.co.uk/jobs/landfill-jobs?pageno=3"]

    def parse(self, response): 
        hrefs = response.xpath("//section[@id='server-results']/article[@class='job-result  ']/a/@href").extract()
        for href in hrefs:
            href = "https://www.reed.co.uk" + href
            yield scrapy.Request(href, callback=self.parse_dir_contents, dont_filter=True)	
			
            
    def parse_dir_contents(self, response):
        item = UniversalSpiderItem()
        item['jobinfo'] = ' '.join(response.xpath("//div[@class='col-xs-12']/h1/text()").extract())
        item['company'] = ' '.join(response.xpath("//div[@class='col-xs-12']/div/a/span/text()").extract())
        item['location'] = ' '.join(response.xpath("//span[@data-qa='localityMobileLbl']/text()").extract()) + ', ' + ' '.join(response.xpath("//span[@data-qa='regionMobileLbl']/text()").extract())
        item['postcode'] = ' '.join(response.xpath("//meta[@itemprop='postalCode']/@content").extract())
        item['description'] = ' '.join(response.xpath("string(//span[@itemprop='description'])").extract())

        yield item
