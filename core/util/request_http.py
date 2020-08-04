# coding:utf-8
import requests
import json


class RequestHttp:
    """
    封装requests发送http请求
    """

    def execute(self, method, url, params=None, body=None, header=None):
        """
        判断并执行具体的http请求
        """
        if method == 'post':
            res = self.__post(url, params, body, header)
        elif method == 'delete':
            res = self.__delete(url, params, header)
        elif method == 'put':
            res = self.__put(url, params, body, header)
        else:
            res = self.__get(url, params, header)
        return res

    def __post(self, url, params, data, header=None):
        """
        发送POST请求
        """
        res = None
        if params is not None:
            url = self.__generate_new_url(url, params)

        if data is not None:
            data = json.dumps(data)

        if header is not None:
            res = requests.post(url=url, data=data, headers=header)
        else:
            res = requests.post(url=url, data=data)
        return res

    def __delete(self, url, params, header=None):
        """
        发送DELETE请求
        """
        if params is not None:
            url = self.__generate_new_url(url, params)

        if header is not None:
            res = requests.delete(url=url, header=header)
        else:
            res = requests.delete(url=url)
        return res

    def __put(self, url, params, data, header=None):
        """
        发送PUT请求
        """
        if params is not None:
            url = self.__generate_new_url(url, params)

        if data is not None:
            data = json.dumps(data)

        res = None
        if header is not None:
            res = requests.put(url=url, data=data, headers=header)
        else:
            res = requests.put(url=url, data=data)
        return res

    def __get(self, url, params=None, header=None):
        """
        发送GET请求
        """
        res = None
        if header is not None:
            res = requests.get(url=url, params=params, headers=header)
        else:
            res = requests.get(url=url, params=params)
        return res

    # 根据url和params生成新的url
    def __generate_new_url(self, url, params):
        loop_count = 0
        for (k, v) in params.items():
            if loop_count == 0:
                url = url + "?"
            else:
                url = url + "&"
            url = url + k + '=' + v
            loop_count = loop_count + 1
        return url
