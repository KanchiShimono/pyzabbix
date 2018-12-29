import json
import urllib.request


class ZabbixAPIException(Exception):
    pass


class ZabbixAPI(object):
    def __init__(self,
                 server):

        self.server = server
        self.url = server + '/api_jsonrpc.php'
        self.auth = ''
        self.id = 0

    def login(self, user='', password=''):
        self.auth = ''
        self.auth = self.user.login(user=user, password=password)

    def do_request(self, method, params=None):

        request_json = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or {},
            'id': self.id,
        }

        if self.auth and (method not in ('apiinfo.version', 'user.login',
                                         'user.checkAuthentication')):
            request_json['auth'] = self.auth

        headers = {
            'Content-Type': 'application/json-rpc',
            'User-Agent': 'python/pyzabbix',
            'Cache-Control': 'no-cache',
        }

        req = urllib.request.Request(self.url,
                                     data=json.dumps(request_json).encode(),
                                     headers=headers,
                                     method='POST')
        with urllib.request.urlopen(req) as res:
            res_str = res.read().decode('utf-8')

        try:
            res_json = json.loads(res_str)
        except ValueError:
            print('Cannot parse res_json')
            raise

        if 'error' in res_json:
            message = 'Error {code}: {message}, {data}'.format(
                code=res_json['error']['code'],
                message=res_json['error']['message'],
                data=res_json['error']['data']
            )

            raise ZabbixAPIException(message)

        return res_json

    def __getattr__(self, name):
        return ZabbixAPIObject(self, name)


class ZabbixAPIObject(object):
    def __init__(self, parent, api_obj):
        self.parent = parent
        self.api_obj = api_obj

    def __getattr__(self, name):

        def fn(*args, **kwargs):
            if args and kwargs:
                raise TypeError('Found both args and kwargs')

            method = '{0}.{1}'.format(self.api_obj, name)

            return self.parent.do_request(
                method,
                args or kwargs
            )['result']

        return fn
