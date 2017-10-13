# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
from collections import OrderedDict
import json


class HttpAPIException(Exception):
    pass


class ReceivedErrorCode(HttpAPIException):
    pass


class ConnectionFailed(HttpAPIException):
    pass


class EuroDollarAPI:

    def __init__(self, host='localhost', user='demo', password='demo'):
        # localhost is only for demo purposes, to make the app run when you are not connected
        # in a real application the euro dollar rate will be given by a distant API
        # to run the demo, copy the euro_dollar_rate.json file in your web folder
        self.host, self.user, self.password = host, user, password

    def get_euro_dollar_rate(self, https=False, lang='en'):
        http_mode = 'https' if https else 'http'
        header = {'Accept-Language': lang}
        url = '%(http_mode)s://%(host)s/API/euro-dollar-rate.json' % {'host': self.host,
                                                                      'http_mode': http_mode}
        try:
            response = requests.get(
                url, auth=HTTPBasicAuth(self.user, self.password,), headers=header)
            if 200 <= response.status_code < 300:
                output = None
                if response.encoding is None:
                    response.encoding = 'UTF-8'
                if len(response.text) > 0:
                    output = json.loads(response.text, object_pairs_hook=OrderedDict)
                return output
            else:
                detail = str(response.status_code)+' - '
                try:
                    if 'detail' in response.json():
                        detail += response.json()['detail']
                except ValueError:
                    detail = 'error '+str(response.status_code)+' at '+' '+url
                raise ReceivedErrorCode(detail)
        except RequestException as e:
            raise ConnectionFailed('request exception  '+type(e).__name__ +' at '+url)
