# coding:utf8
import unittest

import requests
from core.main.run_group_test import RunGroupTest


class Demo(unittest.TestCase):

    def test_case01(self):
        respose = requests.get('http://www.baidu.com')
        print(respose.text)
        self.assertTrue(respose.status_code, '200')
        print('接口正常')

    def test_case02(self):
        runtest = RunGroupTest()
        runtest.go_on_run()
