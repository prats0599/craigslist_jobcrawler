# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ('https://newyork.craigslist.org/search/egr/',
    )

    def parse(self, response):
        listings=response.xpath('//li[@class="result-row"]')
        for listing in listings:
            date=listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            link=listing.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()
            text=listing.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()

            #meta is used to transfer your datapoints from the parse method to parse_lisitng method.its like yield
            yield scrapy.Request(link,callback=self.parse_listing,meta={'date':date,'link':link,'text':text})


        next_pg_url=response.xpath('.//a[@class="button next"]/@href').extract_first()
        next_pg_url=response.urljoin(next_pg_url)
        if next_pg_url:
            yield scrapy.Request(next_pg_url,callback=self.parse)

    def parse_listing(self,response):
        date=response.meta['date']
        link=response.meta['link']
        text=response.meta['text']

        compensation=response.xpath('.//*[@class="attrgroup"]/span[1]/b/text()').extract_first()
        employment_type=response.xpath('.//*[@class="attrgroup"]/span[2]/b/text()').extract_first()

        images=response.xpath('//*[@id="thumbs"]//@src').extract()
        images=[image.replace('50x50c','600x450') for image in images]

        address=response.xpath('.//section[@id="postingbody"]/text()').extract()
        yield{'date':date,
            'link':link,
            'text':text,
            'compensation':compensation,
            'employment_type':employment_type,
            'images':images,
            'address':address
            }
