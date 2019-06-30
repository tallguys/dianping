# -*- coding: utf-8 -*-

import copy
import scrapy
import json
import time
from config import token, uuid, ua, crawl_limit_page, cookies, headers as origin_headers, phone_number
from analytics.predict import predict
from dianping.items import DianpingItem


class ApplyFreeMealsSpider(scrapy.Spider):
    name = 'apply_free_meals'
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

            applyed = activity['applyed']
            yield self.requestDetail(id, applyed)

        pageEnd = data['pageEnd']

        if not pageEnd and self.page <= crawl_limit_page:
            self.page = self.page + 1
            yield self.requestList(self.page)
        else:
            print('page end:' + str(self.page))

    def requestDetail(self, id, applyed):
        url = 'https://m.dianping.com/activity/static/detail?offlineActivityId=' + \
            str(id) + '&token=' + token + '&source=null'

        referer = 'https://h5.dianping.com/app/app-community-free-meal/detail.html?offlineActivityId=' + \
            str(id) + '&token=' + token + \
            '&source=null&utm_source=null&uiwebview=1&product=dpapp&pushEnabled=0'
        headers = copy.deepcopy(origin_headers)
        headers['referer'] = referer

        return scrapy.Request(url=url, callback=self.parseDetail, method='GET', headers=headers, cookies=cookies, meta={'applyed': applyed})

    def parseDetail(self, response):
        jsonResponse = json.loads(response.body.decode(response.encoding))

        data = jsonResponse['data']

        if len(data['detail']['offlineActivityTagDTOList']) > 0:
            tagId = data['detail']['offlineActivityTagDTOList'][0]['tagId']
        else:
            tagId = 0

        features = {
            'cost': data['detail']['cost'],
            'distance': data['detail']['activityShopInfoList'][0]['distance'],
            'score': data['detail']['activityShopInfoList'][0]['shopPower'],
            'tagId': tagId
        }

        activityInfo = {
            'id': data['detail']['offlineActivityId'],
            'title': data['detail']['title'],
            'cost': data['detail']['cost'],
            'shopAddress': data['detail']['activityShopInfoList'][0]['shopAddress'],
            'distanceInfo': data['detail']['activityShopInfoList'][0]['distanceInfo'],
            'distance': data['detail']['activityShopInfoList'][0]['distance'],
            'score': data['detail']['activityShopInfoList'][0]['shopPower'],
            'shopId': data['detail']['activityShopInfoList'][0]['shopId'],
            'shopName': data['detail']['activityShopInfoList'][0]['shopName'],
            'shopType': data['detail']['activityShopInfoList'][0]['shopType'],
        }

        if len(data['detail']['offlineActivityTagDTOList']) > 0:
            activityInfo['tagId'] = data['detail']['offlineActivityTagDTOList'][0]['tagId']
            activityInfo['tagName'] = data['detail']['offlineActivityTagDTOList'][0]['tagName']
        else:
            activityInfo['tagId'] = 0
            activityInfo['tagName'] = ''

        like = predict(features)
        applyed = response.meta['applyed']

        activityInfo['like'] = like

        if like == 1:
            if applyed:
                print('applyed ' + activityInfo['shopName'])
                item = DianpingItem()
                item['id'] = activityInfo['id']
                item['title'] = activityInfo['title']
                item['cost'] = activityInfo['cost']
                item['shopAddress'] = activityInfo['shopAddress']
                item['distanceInfo'] = activityInfo['distanceInfo']
                item['distance'] = activityInfo['distance']
                item['score'] = activityInfo['score']
                item['shopName'] = activityInfo['shopName']
                item['shopType'] = activityInfo['shopType']
                item['tagId'] = activityInfo['tagId']
                item['tagName'] = activityInfo['tagName']
                item['like'] = activityInfo['like']
                item['apply_result'] = '成功'

                yield item
            else:
                yield self.requestGetPreApply(activityInfo)

    def requestGetPreApply(self, activityInfo):
        activityId = activityInfo['id']
        shopId = activityInfo['shopId']

        url = 'https://m.dianping.com/mobile/dinendish/apply/getPreApply'

        referer = 'https://m.dianping.com/mobile/dinendish/apply/' + \
            str(activityId) + '?a=1&source=null&utm_source=null&showShopId=' + \
            str(shopId) + '&token=' + token + \
            '&uiwebview=1&product=dpapp&pushEnabled=0'
        headers = copy.deepcopy(origin_headers)
        headers['referer'] = referer

        body = {
            'activityId': activityId,
            'token': token,
            'env': 4
        }

        return scrapy.Request(url=url, callback=self.parseGetPreApply, method='GET', headers=headers, cookies=cookies, body=json.dumps(body), meta={'activityInfo': activityInfo})

    def parseGetPreApply(self, response):
        activityInfo = response.meta['activityInfo']
        activityId = activityInfo['id']
        shopId = activityInfo['shopId']

        yield self.requestDoApply(activityInfo)

    def requestDoApply(self, activityInfo):
        activityId = activityInfo['id']
        shopId = activityInfo['shopId']

        url = 'https://m.dianping.com/mobile/dinendish/apply/doApplyActivity'

        referer = 'https://m.dianping.com/mobile/dinendish/apply/' + \
            str(activityId) + '?a=1&source=null&utm_source=null&showShopId=' + \
            str(shopId) + '&token=' + token + \
            '&uiwebview=1&product=dpapp&pushEnabled=0'
        headers = copy.deepcopy(origin_headers)
        headers['referer'] = referer

        body = {
            'passCardNo': '',
            'phoneNo': phone_number,
            'cx': '',
            'uuid': uuid,
            'offlineActivityId': activityId,
            'env': 4,
            'source': 'null'
        }

        return scrapy.Request(url=url, callback=self.parseDoApply, method='GET', headers=headers, cookies=cookies, body=json.dumps(body), meta={'activityInfo': activityInfo})

    def parseDoApply(self, response):
        jsonResponse = json.loads(response.body.decode(response.encoding))

        data = jsonResponse['data']

        activityInfo = response.meta['activityInfo']

        item = DianpingItem()
        item['id'] = activityInfo['id']
        item['title'] = activityInfo['title']
        item['cost'] = activityInfo['cost']
        item['shopAddress'] = activityInfo['shopAddress']
        item['distanceInfo'] = activityInfo['distanceInfo']
        item['distance'] = activityInfo['distance']
        item['score'] = activityInfo['score']
        item['shopName'] = activityInfo['shopName']
        item['shopType'] = activityInfo['shopType']
        item['tagId'] = activityInfo['tagId']
        item['tagName'] = activityInfo['tagName']
        item['like'] = activityInfo['like']
        item['apply_result'] = data['desc']

        yield item
