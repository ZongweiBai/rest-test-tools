# coding:utf-8
import requests


class RequestHttp:

    # 发送POST请求
    def post(self, url, data, header=None):
        res = None
        if header is not None:
            res = requests.post(url=url, data=data, headers=header)
        else:
            res = requests.post(url=url, data=data)
        return res.json()

    # 发送DELETE请求
    def delete(self, url, header=None):
        if header is not None:
            res = requests.delete(url=url, header=header)
        else:
            res = requests.delete(url=url)
        return res.json()

    # 发送PUT请求
    def put(self, url, data, header=None):
        res = None
        if header is not None:
            res = requests.put(url=url, data=data, headers=header)
        else:
            res = requests.put(url=url, data=data)
        return res.json()

    # 发送GET请求
    def get(self, url, params=None, header=None):
        res = None
        if header is not None:
            res = requests.get(url=url, params=params, headers=header)
        else:
            res = requests.get(url=url, params=params)
        return res.json()

    # 判断并执行具体的请求
    def execute(self, method, url, data=None, header=None, params=None):
        res = None
        if method == 'post':
            res = self.post(url, data, header)
        elif method == 'delete':
            res = self.delete(url, header)
        elif method == 'put':
            res = self.put(url, params, header)
        else:
            res = self.get(url, params, header)
        return res
