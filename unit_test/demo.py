# coding:utf8
import requests
import unittest


class Demo(unittest.TestCase):

    def test_case01(self):
        respose = requests.get('http://www.baidu.com')
        print(respose.text)
        self.assertTrue(respose.status_code, '200')
        print('接口正常')
