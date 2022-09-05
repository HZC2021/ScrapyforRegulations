import json

import scrapy

from regulations.items import RegulationsItem, RegulationsDetailItem


class RegulationSpider(scrapy.Spider):
    name = 'regulation'
    allowed_domains = ['regulations.gov']
    did = 'ED-2021-OCR-0166'
    start_urls = [f'https://api.regulations.gov/v4/dockets/{did}']
    list_urls = 'https://api.regulations.gov/v4/comments?filter%5BdocketId%5D={}&page%5Bnumber%5D={}'
    comment_url = 'https://api.regulations.gov/v4/comments/{}?include=attachments'

    def parse(self, response):
        reg_item = RegulationsItem()
        resp_list = response.json()
        if resp_list:
            print('====title:'+resp_list['data']['attributes']['title'])
            print('====date:'+resp_list['data']['attributes']['modifyDate'])
            
            reg_item['title'] = resp_list['data']['attributes']['title']
            reg_item['postDate'] = resp_list['data']['attributes']['modifyDate']
            reg_item['rid'] = resp_list['data']['id']
            yield reg_item
            for i in range(1,3):
                # print(i)
                url = self.list_urls.format(self.did,i)
                yield scrapy.Request(url=url,callback=self.parse_list)

    def parse_list(self,response):
        comments = response.json()
        for comment in comments['data']:
            cid = comment['id']
            # post_data = comment['attributes']['postedDate']
            comment_url = self.comment_url.format(cid)
            yield scrapy.Request(url=comment_url,callback=self.parse_detail)

    def parse_detail(self,response):
        detail_item = RegulationsDetailItem()
        detail = response.json()
        # print('====id:'+detail['data']['id'])
        # print('====comment:'+detail['data']['attributes']['comment'])
        # print('====comment postdate:'+detail['data']['attributes']['postedDate'])
        # print('====poster:'+detail['data']['attributes']['firstName']+' '+detail['data']['attributes']['lastName'])

        detail_item['cid'] = detail['data']['id']
        detail_item['comment'] = detail['data']['attributes']['comment']
        detail_item['postDate'] = detail['data']['attributes']['postedDate']
        detail_item['poster'] = detail['data']['attributes']['firstName']+' '+detail['data']['attributes']['lastName']
        yield detail_item
