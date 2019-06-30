# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv


class DianpingPipeline(object):
    filename = 'dianping.csv'
    fieldnames = [
        'id',
        'title',
        'cost',
        'shopAddress',
        'distanceInfo',
        'distance',
        'score',
        'shopName',
        'shopType',
        'tagId',
        'tagName',
        'like',
        'apply_result',
    ]

    def __init__(self):
        with open(self.filename, 'w', encoding='utf8') as f:
            csv_writer = csv.DictWriter(
                f, fieldnames=self.fieldnames)
            csv_writer.writeheader()

    def process_item(self, item, spider):
        with open(self.filename, 'a', encoding='utf8') as f:
            csv_writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            csv_writer.writerow(item)

        return item
