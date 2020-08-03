# coding:utf-8
import requests


class RequestHttp:

    # 发送POST请求
    def post(self, url, params, data, header=None):
        res = None
        if params is not None:
            url = self.__generate_new_url(url, params)

        if header is not None:
            res = requests.post(url=url, data=data, headers=header)
        else:
            res = requests.post(url=url, data=data)
        return res

    # 发送DELETE请求
    def delete(self, url, params, header=None):
        if params is not None:
            url = self.__generate_new_url(url, params)

        if header is not None:
            res = requests.delete(url=url, header=header)
        else:
            res = requests.delete(url=url)
        return res

    # 发送PUT请求
    def put(self, url, params, data, header=None):
        if params is not None:
            url = self.__generate_new_url(url, params)

        res = None
        if header is not None:
            res = requests.put(url=url, data=data, headers=header)
        else:
            res = requests.put(url=url, data=data)
        return res

    # 发送GET请求
    def get(self, url, params=None, header=None):
        res = None
        if header is not None:
            res = requests.get(url=url, params=params, headers=header)
        else:
            res = requests.get(url=url, params=params)
        return res

    # 判断并执行具体的请求
    def execute(self, method, url, params=None, body=None, header=None):
        if method == 'post':
            res = self.post(url, params, body, header)
        elif method == 'delete':
            res = self.delete(url, params, header)
        elif method == 'put':
            res = self.put(url, params, body, header)
        else:
            res = self.get(url, params, header)
        return res

    # 根据url和params生成新的url
    def __generate_new_url(self, url, params):
        return url
