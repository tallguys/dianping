# -*- coding: utf-8 -*-

import copy
import scrapy
import json
from config import token, crawl_limit_page, cookies, ua, headers as origin_headers
from dianping.items import DianpingItem


class FreeMealsSpider(scrapy.Spider):
    name = 'list_free_meals'
    page = 1

    def start_requests(self):
        yield self.requestList(self.page)

    def requestList(self, page):
        url = 'https://m.dianping.com/activity/static/list?page=' + \
            str(page) + '&cityid=7&latitude=22.57678&longitude=114.13430&regionParentId=0&regionId=0&type=0&sort=0&filter=0&token=' + token

        referer = 'https://h5.dianping.com/app/app-community-free-meal/index.html?notitlebar=1&cityid=7&latitude=22.57678&longitude=114.13430&cityid=7&ci=*&lat=*&lng=*&infrom=dpshouye&product=dpapp&pushEnabled=0'
        headers = copy.deepcopy(origin_headers)
        headers['referer'] = referer

        return scrapy.Request(url=url, callback=self.parseList, method='GET', headers=headers, cookies=cookies)

    def parseList(self, response):
        jsonResponse = json.loads(response.body.decode(response.encoding))

        data = jsonResponse['data']

        activitys = data['mobileActivitys']

        for activity in activitys:
            id = activity['offlineActivityId']
            yield self.requestDetail(id)

        pageEnd = data['pageEnd']

        if not pageEnd and self.page <= crawl_limit_page:
            self.page = self.page + 1
            yield self.requestList(self.page)
        else:
            print('page end:' + str(self.page))

    def requestDetail(self, id):
        url = 'https://m.dianping.com/activity/static/detail?offlineActivityId=' + \
            str(id) + '&token=' + token + '&source=null'

        referer = 'https://h5.dianping.com/app/app-community-free-meal/detail.html?offlineActivityId=' + \
            str(id) + '&token=' + token + \
            '&source=null&utm_source=null&uiwebview=1&product=dpapp&pushEnabled=0'
        headers = copy.deepcopy(origin_headers)
        headers['referer'] = referer

        return scrapy.Request(url=url, callback=self.parseDetail, method='GET', headers=headers, cookies=cookies)

    def parseDetail(self, response):
        jsonResponse = json.loads(response.body.decode(response.encoding))

        data = jsonResponse['data']

        item = DianpingItem()
        item['id'] = data['detail']['offlineActivityId']
        item['title'] = data['detail']['title']
        item['cost'] = data['detail']['cost']
        item['shopAddress'] = data['detail']['activityShopInfoList'][0]['shopAddress']
        item['distanceInfo'] = data['detail']['activityShopInfoList'][0]['distanceInfo']
        item['distance'] = data['detail']['activityShopInfoList'][0]['distance']
        item['score'] = data['detail']['activityShopInfoList'][0]['shopPower']
        item['shopName'] = data['detail']['activityShopInfoList'][0]['shopName']
        item['shopType'] = data['detail']['activityShopInfoList'][0]['shopType']

        if len(data['detail']['offlineActivityTagDTOList']) > 0:
            item['tagId'] = data['detail']['offlineActivityTagDTOList'][0]['tagId']
            item['tagName'] = data['detail']['offlineActivityTagDTOList'][0]['tagName']
        else:
            item['tagId'] = 0
            item['tagName'] = ''

        item['like'] = ''
        item['apply_result'] = ''

        yield item
