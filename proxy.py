# -*- coding: utf-8 -*-


class Proxy(object):
    def __init__(self):
        self.id = 1
        self.ip = ''
        self.port = ''
        self.country = ''
        self.anonymity = ''
        self.https = ''
        self.speed = ''
        self.source = ''
        self.vali_count = 0

    def __str__(self):
        data = {
            'ip': self.ip,
            'port': self.port,
            'country': self.country,
            'anonymity': self.anonymity,
            'https': self.https,
            'speed': self.speed,
            'source': self.source,
            'vali_count': self.vali_count,
        }

        return str(data)

    def __dict__(self):
        data = {
            'ip': self.ip,
            'port': self.port,
            'country': self.country,
            'anonymity': self.anonymity,
            'https': self.https,
            'speed': self.speed,
            'source': self.source,
            'vali_count': self.vali_count,
        }

        return data

    def get_dict(self):
        data = {
            'ip': self.ip,
            'port': self.port,
            'country': self.country,
            'anonymity': self.anonymity,
            'https': self.https,
            'speed': self.speed,
            'source': self.source,
            'vali_count': self.vali_count,
        }

        return data

    def set_value(self, ip, port, country, anonymity, source='unkonw', https='no', speed=-1, vali_count=0):
        self.ip = ip
        self.port = port
        self.country = country
        self.anonymity = self.get_anonymity_type(anonymity)
        self.https = https
        self.speed = speed
        self.source = source
        self.vali_count = vali_count

    def get_anonymity_type(self, anonymity):
        '''There are 3 levels of proxies according to their anonymity.

            Level 1 - Elite Proxy / Highly Anonymous Proxy: The web server can't detect whether you are using a proxy.
            Level 2 - Anonymous Proxy: The web server can know you are using a proxy, but it can't know your real IP.
            Level 3 - Transparent Proxy: The web server can know you are using a proxy and it can also know your real
            IP.
        '''
        anonymity = str(anonymity).strip()
        if anonymity == '高匿代理' or anonymity == '高匿名' or anonymity == 'elite proxy' or \
                        anonymity == '超级匿名' or anonymity == 'High' or anonymity == '高匿' or anonymity == '1':
            return '1'
        elif anonymity == '匿名' or anonymity == 'anonymous' or anonymity == '普通匿名' or anonymity == 'Medium' or anonymity == '2':
            return '2'
        elif anonymity == '透明' or anonymity == 'transparent' or anonymity == 'No' or anonymity == '3':
            return '3'
        else:
            return '3'
