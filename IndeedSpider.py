#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 14:25:14 2019

@author: luhao
"""

import scrapy
from Indeed_jobsite.items import UniversalSpiderItem



class IndeedSpider(scrapy.Spider):
    name = "IndeedSpider"
    allowed_domains = ['indeed.co.uk']
    start_urls = ["https://www.indeed.co.uk/jobs?q=landfill&start="]
    npages = [i for i in range(1, 24)]
    for i in npages:
        start_urls.append("https://www.indeed.co.uk/jobs?q=landfill&start="+str(i*10)+"")
        
    def parse(self, response): 
        hrefs = response.xpath("//div[@data-tu]/h2[@class='jobtitle']/a/@href|//div[@data-tu]/a/@href").extract()
        for href in hrefs:
            if href.startswith("http") is False:
                href = "https://www.indeed.co.uk" + href
                #t=1
                #time.sleep(t)
                yield scrapy.Request(href, callback=self.parse_dir_contents)	
			
            
    def parse_dir_contents(self, response):
        item = UniversalSpiderItem()
        item['jobinfo'] = ' '.join(response.xpath("//h3/text()").extract())
        item['company'] = ' '.join(response.xpath("//div[@class='jobsearch-InlineCompanyRating icl-u-xs-mt--xs  jobsearch-DesktopStickyContainer-companyrating']/div[1]/text()").extract())
        item['location'] = ' '.join(response.xpath("//div[@class='jobsearch-InlineCompanyRating icl-u-xs-mt--xs  jobsearch-DesktopStickyContainer-companyrating']/div[not(@*)]/text()").extract())
        item['postcode'] = 'Not available'
        item['description'] = ' '.join(response.xpath("string(//div[@class='jobsearch-JobComponent-description icl-u-xs-mt--md'])").extract())

        yield item
