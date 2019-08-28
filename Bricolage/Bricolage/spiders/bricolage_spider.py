# -*- coding: utf-8 -*-
import scrapy
from ..items import BricolageItem


class BricolageSpiderSpider(scrapy.Spider):
    name = 'bricolage'
    start_urls = [
        'https://mr-bricolage.bg/bg/Instrumenti/Avto-i-veloaksesoari/\
        Veloaksesoari/c/006008012'
    ]

    def parse(self, response):
        product_urls = response.css('div.title a::attr(href)').getall()
        for url in product_urls:
            link = 'https://mr-bricolage.bg' + url
            yield scrapy.Request(link, callback=self.parse_each_element)

        next_page = response.css('li.pagination-next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_each_element(self, response):

        items = BricolageItem()

        product_title = self.filter_text(
            response.css('.js-product-name::text').extract())
        product_price = self.filter_price(
            response.css('.js-product-price').css('::text').extract())
        product_imagelink = self.filter_text(
            response.css(
                '.owl-carousel-thumbs img::attr(src)').extract())
        product_characteristic = self.filter_characteristic(
            response.css('.table tr td').css('::text').extract())

        # number = response.css('.bricolage-code::text').extract_first()
        # num = [int(s) for s in number.split() if s.isdigit()]
        # request_text = '#pickupModal_product_{} > div.pickup-component >\
        #  div.js-find-store-display > div.store-navigation >\
        #   ul.js-pickup-store-list > li.pickup-store-list-entry >\
        #    label.js-select-store-label > span.pickup-store-info >\
        #     span.pickup-store-list-entry-name'.format(
        #     num[0])
        # print(request_text, '===',
        #       response.css(request_text).extract_first())

        items['product_title'] = product_title
        items['product_price'] = product_price
        items['product_imagelink'] = product_imagelink
        items['product_characteristic'] = product_characteristic

        yield items

    def filter_text(self, list):
        result = []
        for line in list:
            result.append(line.strip())
        return result

    def filter_price(self, list):
        result = []
        for line in list:
            result.append(line.replace('лв.', '').replace(',', '.').strip())
        return result

    def filter_characteristic(self, list):
        result = []
        for line in list:
            result.append(line.replace('\n', '').replace('\t', '').strip())
        return result
