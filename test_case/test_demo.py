# coding:utf8
import os
import unittest

import requests
import json

from core.main.run_group_test import RunGroupTest
from core.core_config import CoreConfig


class Demo(unittest.TestCase):

    def test_case01(self):
        respose = requests.get('http://www.baidu.com')
        print(respose.text)
        self.assertTrue(respose.status_code, '200')
        print('接口正常')

    def test_oauth_acl(self):
        core_config = CoreConfig()
        runtest = RunGroupTest(os.path.join(core_config.test_case_file_path, 'oauth_server_test.xls'), 0)
        runtest.go_on_run()

    def test_json_load(self):
        file_header_dict = {
          "Accept": "application/json, text/javascript, */*; q=0.01",
          "Accept-Encoding": "gzip, deflate, br",
          "Accept-Language": "zh-CN,zh;q=0.8",
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400",
          "Connection": "keep-alive",
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

        # file_header_dict = json.load(json_string)

        request_header = {
         "clientId": "fs_client",
         "dailyMaxAccess": 1000,
         "allowList": "0.0.0.0",
         "blockList": "192.168.111.128"
        }

        # request_header = json.load(request_string)
        request_header.update(file_header_dict)
        print(request_header)
