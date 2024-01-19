import requests
import json
from requests.auth import HTTPBasicAuth
import argparse
from os import environ
import random
import string

default_headers = {'Content-Type': 'application/json'}

class Instance:
    def __init__(self,
                 rabbitmq_host=environ.get('RABBITMQ_HOST') or '127.0.0.1',
                 rabbitmq_port=environ.get('RABBITMQ_PORT') or '15672',
                 rabbitmq_admin_user=environ.get('RABBITMQ_ADMIN_USER') or 'guest',
                 rabbitmq_admin_password=environ.get('RABBITMQ_ADMIN_PASSWORD)') or 'guest',
                 rabbitmq_tls_enabled=environ.get('RABBITMQ_TLS_ENABLED') or False
                 ):
        if rabbitmq_tls_enabled:
            rabbitmq_scheme = 'https://'
        else:
            rabbitmq_scheme = 'http://'
        self.rabbitmq_baseurl = rabbitmq_scheme + rabbitmq_host + ':' + str(rabbitmq_port) + '/api'
        self.rabbitmq_auth = HTTPBasicAuth(rabbitmq_admin_user, rabbitmq_admin_password)

    class VirtualHost:
        @staticmethod
        def create(vhost):
            http_method = 'PUT'
            description = f"Description_for_{vhost}"
            tags = f"Tags_{vhost}"
            service = 'vhosts'
            headers = default_headers
            data = {
                'description': description,
                'tags': tags
            }
            baseurl = Instance().rabbitmq_baseurl
            url = f"{baseurl}/{service}/{vhost}"
            auth = Instance().rabbitmq_auth
            print(f"Talking to URL: {url}")
            r = requests.request(http_method, url,data=json.dumps(data),headers=headers,auth=auth)
            print(r.status_code)

        @staticmethod
        def delete(vhost):
            http_method = 'DELETE'
            service = 'vhosts'
            headers = default_headers
            auth = Instance().rabbitmq_auth
            baseurl = Instance().rabbitmq_baseurl
            url = f"{baseurl}/{service}/{vhost}"
            print(f"Talking to URL: {url}")
            r = requests.request(http_method, url, headers=headers,auth=auth)
            print(r.status_code)
    class User:
        @staticmethod
        def create(user, password=None):
            http_method = 'PUT'
            tags = f"Tags-{user}"
            service = 'users'
            headers = default_headers
            if password is None:
                password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
                print(f"Generating password for user: {user}, password: {password}")
            data = {
                'password': password,
                'tags': tags
            }
            auth = Instance().rabbitmq_auth
            baseurl = Instance().rabbitmq_baseurl
            url = f"{baseurl}/{service}/{user}"
            print(f"Talking to URL: {baseurl}, {url}")
            r = requests.request(http_method, url, data=json.dumps(data), headers=headers,auth=auth)
            print(r.status_code)

        @staticmethod
        def delete(user):
            http_method = 'DELETE'
            service = 'users'
            headers = default_headers
            auth = Instance().rabbitmq_auth
            baseurl = Instance().rabbitmq_baseurl
            url = f"{baseurl}/{service}/{user}"
            print(f"Talking to URL: {baseurl}, {url}")
            r = requests.request(http_method, url, headers=headers,auth=auth)
            print(r.status_code)
    class Exchange:
        @staticmethod
        def create(vhost=None, exchange=None, exchange_type=None, durable=True):
            # /api/exchanges/vhost/name
            if exchange_type not in ["direct", "fanout", "topic"]:
                exchange_type = 'fanout'
            http_method = 'PUT'
            service = 'exchanges'
            headers = default_headers
            data = {
                "type": exchange_type,
                "auto_delete": False,
                "durable": durable,
                "internal": False,
                "arguments": {}
            }
            auth = Instance().rabbitmq_auth
            baseurl = Instance().rabbitmq_baseurl
            url = f"{baseurl}/{service}/{vhost}/{exchange}"
            print(f"Talking to URL: {url}")
            r = requests.request(http_method, url, data=json.dumps(data), headers=headers,auth=auth)
            print(r.status_code)
        @staticmethod
        def delete(vhost=None,exchange=None):
            http_method = 'DELETE'
            service = 'exchanges'
            headers = default_headers
            auth = Instance().rabbitmq_auth
            baseurl = Instance().rabbitmq_baseurl
            url = f"{baseurl}/{service}/{vhost}/{exchange}"
            print(f"Talking to URL: {url}")
            r = requests.request(http_method, url, headers=headers,auth=auth)
            print(r.status_code)     
    class Binding:
        pass
