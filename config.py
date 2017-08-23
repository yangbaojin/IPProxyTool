# coding=utf-8

DB_config = {
    # 'db_type': 'mongodb',
    # 'db_type': 'mysql',
    'db_type': 'sqlite',

    'mysql': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',
        'charset': 'utf8',
    },
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'password': '',
        'db': 1,
    },
    'mongodb':{
        'host': 'localhost',
        'port': 27017,
        'username': '',
        'password': '',
    },
    'sqlite':{
            'database': 'proxytool.db',
    }

}

database = 'ipproxy'
free_ipproxy_table = 'free_ipproxy'
httpbin_table = 'httpbin'

data_port = 8000
