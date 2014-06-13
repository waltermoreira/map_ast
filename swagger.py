import json
import os
import urlparse

import requests


class Swagger(object):

    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse.urlparse(url)
        self.get = (self.file_get if self.parsed_url.scheme == 'file'
                    else self.requests_get)
        self.index = index = self.get('index.html')
        self.apis = {}
        for api in index['apis']:
            path = api['path']
            name = os.path.basename(path)
            self.apis[name] = self.get(name)

    def file_get(self, path):
        f = open(os.path.join(self.parsed_url.path, path))
        return json.load(f)

    def requests_get(self, path):
        resp = requests.get(urlparse.urljoin(self.url, path))
        if resp.ok:
            return resp.json()

    def get_nickname(self, nickname, endpoint):
        apis = self.apis[endpoint]['apis']
        for api in apis:
            url_path = api['path']
            for operation in api['operations']:
                if operation['nickname'] == nickname:
                    return {'path': url_path,
                            'operation': operation}
        raise Exception('nickname "{}" not found'.format(nickname))

    def get_parameter(self, name, nickname, endpoint):
        parameters = self.get_nickname(
            nickname, endpoint)['operation']['parameters']
        for parameter in parameters:
            if parameter['name'] == name:
                return parameter
        raise Exception('parameter "{}" not found'.format(name))

    def get_model(self, name, endpoint):
        return self.apis[endpoint]['models'][name]
