#-*- coding: utf-8 -*-

import re

from proxy import Proxy
from .basespider import BaseSpider


class KuaiDaiLiSpider(BaseSpider):
    name = 'kuaidaili'

    def __init__(self, *a, **kwargs):
        super(KuaiDaiLiSpider, self).__init__(*a, **kwargs)

        self.urls = ['http://www.kuaidaili.com/free/inha/%s/' % i for i in range(1, 5)]

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "www.kuaidaili.com",
            "Referer": "http://www.kuaidaili.com/free/inha/1/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
        }

        self.is_record_web_page = False
        self.init()

    def parse_page(self, response):
        pattern = re.compile(
                '<tr>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>('
                '.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?</tr>',
                re.S)
        items = re.findall(pattern, response.body.decode('utf-8'))
        # print(items)
        for item in items:
            proxy = Proxy()
            proxy.set_value(
                    ip = item[0],
                    port = item[1],
                    country = item[4],
                    anonymity = item[2],
                    source = self.name,
            )
            self.add_proxy(proxy)
