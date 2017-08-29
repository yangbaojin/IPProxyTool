# -*- coding: utf-8 -*-

import logging
import utils
import config
import sqlite3
import time

from proxy import Proxy
from sql.sql import Sql


class Sqlite(Sql):
    def __init__(self, **kwargs):
        super(Sqlite, self).__init__(**kwargs)

        self.conn = sqlite3.connect(**kwargs)
        self.cursor = self.conn.cursor()

        # try:
        #     self.conn.select_db(config.database)
        # except:
        #     self.create_database(config.database)
        #     self.conn.select_db(config.database)

    def create_database(self, database_name):
        pass

    def init_database(self, database_name):
        pass

    def init_proxy_table(self, table_name):
        pass

    def insert_proxy(self, table_name, proxy):
        try:
            if self.select_proxy_ip(table_name, proxy.ip):
                return True
            command = ("INSERT INTO {} "
                       "(id, ip, port, country, anonymity, https, speed, source, save_time, vali_count)"
                       "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table_name))
            data = (None, proxy.ip, proxy.port, proxy.country, proxy.anonymity,
                    proxy.https, proxy.speed, proxy.source, int(time.time()), proxy.vali_count)
            self.cursor.execute(command, data)
            return True
        except Exception as e:
            print(e)
            logging.exception('mysql insert_proxy exception msg:%s' % e)
            return False

    def select_proxy_ip(self, table_name, ip):
        try:
            command = "SELECT * FROM {name} WHERE ip='{ip}'".format(name=table_name, ip=ip)
            result = self.query(command)
            if result:
                return result
            else:
                return
        except Exception as e:
            logging.exception('mysql select_proxy exception msg:%s' % e)
            return

    def select_proxy(self, table_name, **kwargs):
        filter = {}
        for k, v in kwargs.items():
            if v != '':
                filter[k] = v

        try:
            command = "SELECT * FROM {name} WHERE anonymity LIKE '{anonymity}' AND https LIKE '{https}' ORDER BY " \
                      "{order} {sort} limit {count}". \
                format(name=table_name, anonymity=filter.get('anonymity', '%'),
                       https=filter.get('https', '%'), order=filter.get('order', 'save_time'),
                       sort=filter.get('sort', 'desc'), count=filter.get('count', 100))

            result = self.query(command)
            data = [{
                'ip': item[1], 'port': item[2], 'anonymity': item[4], 'https': item[5],
                'speed': item[6], 'save_time': str(item[8])
            } for item in result]
            return data
        except Exception as e:
            logging.exception('mysql select_proxy exception msg:%s' % e)
        return []

    def update_proxy(self, table_name, proxy):
        try:
            command = "UPDATE {table_name} set https='{https}', speed={speed}, " \
                      "vali_count={vali_count}, anonymity = {anonymity},save_time={save_time} " \
                      "where id={id};".format(
                table_name=table_name, https=proxy.https,
                speed=proxy.speed, id=proxy.id, vali_count=proxy.vali_count, anonymity=proxy.anonymity,
                save_time=int(time.time()))
            logging.debug('mysql update_proxy command:%s' % command)
            self.cursor.execute(command)
        except Exception as e:
            logging.exception('mysql update_proxy exception msg:%s' % e)

    def delete_proxy(self, table_name, proxy):
        self.del_proxy_with_id(table_name=table_name, id=proxy.id)

    def delete_old(self, table_name, day):
        try:
            command = "DELETE FROM {table} where save_time < {now_time}".format(
                table=config.free_ipproxy_table, now_time=int(time.time())-3600*24)

            self.cursor.execute(command)
            self.commit()
        except Exception as e:
            print(e)
            logging.exception('mysql delete_old exception msg:%s' % e)

    def get_proxy_count(self, table_name):
        try:
            command = "SELECT COUNT(*) from {0}".format(table_name)
            count, = self.query_one(command)
            logging.debug('mysql get_proxy_count count:%s' % count)
            return count
        except Exception as e:
            logging.exception('mysql get_proxy_count exception msg:%s' % e)

        return 0

    def get_proxy_ids(self, table_name):
        ids = []
        try:
            command = "SELECT id from {}".format(table_name)
            result = self.query(command)
            ids = [item[0] for item in result]
        except Exception as e:
            logging.exception('mysql get_proxy_ids exception msg:%s' % e)

        return ids

    def get_proxy_with_id(self, table_name, id):
        proxy = Proxy()
        try:
            command = "SELECT * FROM {0} WHERE id=\'{1}\'".format(table_name, id)
            result = self.query_one(command)
            if result != None:
                # data = {
                #     'id': result[0],
                #     'ip': result[1],
                #     'port': result[2],
                #     'country': result[3],
                #     'anonymity': result[4],
                #     'https': result[5],
                #     'speed': result[6],
                #     'source': result[7],
                #     'save_time': result[8],
                #     'vali_count': result[9],
                # }
                proxy = Proxy()
                proxy.set_value(
                    ip=result[1],
                    port=result[2],
                    country=result[3],
                    anonymity=result[4],
                    https=result[5],
                    speed=result[6],
                    source=result[7],
                    vali_count=result[9])
                proxy.id = result[0]
                proxy.save_time = result[8]
        except Exception as e:
            logging.exception('mysql get_proxy_ids exception msg:%s' % e)

        return proxy

    def del_proxy_with_id(self, table_name, id):
        res = False
        try:
            command = "DELETE FROM {0} WHERE id={1}".format(table_name, id)
            self.cursor.execute(command)
            res = True
        except Exception as e:
            logging.exception('mysql get_proxy_ids exception msg:%s' % e)

        return res

    def del_proxy_with_ip(self, table_name, ip):
        res = False
        try:
            command = "DELETE FROM {0} WHERE ip='{1}'".format(table_name, ip)
            self.cursor.execute(command)
            self.commit()
            res = True
        except Exception as e:
            logging.exception('mysql del_proxy_with_ip exception msg:%s' % e)

        return res

    def create_table(self, command):
        try:
            logging.debug('mysql create_table command:%s' % command)
            x = self.cursor.execute(command)
            self.conn.commit()
            return x
        except Exception as e:
            logging.exception('mysql create_table exception:%s' % e)

    def insert_data(self, command, data, commit=False):
        try:
            logging.debug('mysql insert_data command:%s, data:%s' % (command, data))
            x = self.cursor.execute(command, data)
            if commit:
                self.conn.commit()
            return x
        except Exception as e:
            logging.debug('mysql insert_data exception msg:%s' % e)

    def commit(self):
        self.conn.commit()

    def execute(self, command, commit=True):
        try:
            logging.debug('mysql execute command:%s' % command)
            data = self.cursor.execute(command)
            if commit:
                self.conn.commit()
            return data
        except Exception as e:
            logging.exception('mysql execute exception msg:%s' % e)
            return None

    def query(self, command, commit=False):
        try:
            logging.debug('mysql execute command:%s' % command)

            self.cursor.execute(command)
            data = self.cursor.fetchall()
            if commit:
                self.conn.commit()
            return data
        except Exception as e:
            logging.exception('mysql execute exception msg:%s' % e)
            return None

    def query_one(self, command, commit=False):
        try:
            logging.debug('mysql execute command:%s' % command)

            self.cursor.execute(command)
            data = self.cursor.fetchone()
            if commit:
                self.conn.commit()

            return data
        except Exception as e:
            logging.debug('mysql execute exception msg:%s' % str(e))
            return None
