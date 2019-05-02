#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 13:19:51 2019

@author: luhao
"""

import scrapy
from Indeed_jobsite.items import UniversalSpiderItem


class ReedSpider(scrapy.Spider):
    name = "CVSpider"
    allowed_domains = ['cv-library.co.uk']
    start_urls = ["https://www.cv-library.co.uk/search-jobs?distance=15&fp=1&geo=&posted=&q=landfill&salarymax=&salarymin=&salarytype=annum&search=1&tempperm=Any", 
                  "https://www.cv-library.co.uk/search-jobs?distance=15&fp=1&geo=&offset=25&posted=&q=landfill&salarymax=&salarymin=&salarytype=annum&search=1&tempperm=Any", 
                  "https://www.cv-library.co.uk/search-jobs?distance=15&fp=1&geo=&offset=50&posted=&q=landfill&salarymax=&salarymin=&salarytype=annum&search=1&tempperm=Any",
                  "https://www.cv-library.co.uk/search-jobs?distance=15&fp=1&geo=&offset=75&posted=&q=landfill&salarymax=&salarymin=&salarytype=annum&search=1&tempperm=Any"]

    def parse(self, response): 
        hrefs = response.xpath("//div[@class='job-search-details']/a/@href").extract()
        for href in hrefs:
            href = "https://www.cv-library.co.uk" + href
            yield scrapy.Request(href, callback=self.parse_dir_contents, meta = {'dont_redirect': True}, dont_filter=True)	
			
            
    def parse_dir_contents(self, response):
        item = UniversalSpiderItem()
        if response.xpath("//div[@class='cvl-feat-sash']") != []:
            item['jobinfo'] = ' '.join(response.xpath("string(//div[@id='cvl-feat-job-highlight']/h1)").extract())
            item['company'] = ' '.join(response.xpath("//div[@id='js-company-details']/a/text()").extract())
            item['location'] = ' '.join(response.xpath("//div[@id='js-loc-details']/text()").extract())
            item['postcode'] = 'Not available'
            item['description'] = ' '.join(response.xpath("string(//div[@id='cvl-feat-job-main']/div[@id='cvl-feat-job-desc'])").extract())
        if response.xpath("//div[@class='cvl-feat-sash']") == []:
            item['jobinfo'] = ' '.join(response.xpath("string(//h1[@class='jobTitle'])").extract())
            item['company'] = ' '.join(response.xpath("string(//div[@id='js-company-details']/a)").extract())
            item['location'] = ' '.join(response.xpath("//div[@id='job-location']/text()").extract())
            item['postcode'] = 'Not available'
            item['description'] = ' '.join(response.xpath("string(//div[@class='jd-details jobview-desc'])").extract())

        yield item
