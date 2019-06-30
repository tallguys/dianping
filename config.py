# -*- coding: utf-8 -*-

import os
import json

# token
token = os.environ['TOKEN']

# max crawling page
crawl_limit_page = int(os.environ['CRAWL_LIMIT_PAGE'])

# uuid
uuid = os.environ['UUID']

# ua
ua = os.environ['UA']

# cookies
cookies = json.loads(os.environ['COOKIES'])

# headers
headers = {
    'host': 'm.dianping.com',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://h5.dianping.com',
    'accept': 'application/json, text/javascript',
    'user-agent': ua,
    'accept-language': 'zh-cn',
}

# phone
phone_number = os.environ['PHONE_NUMBER']
