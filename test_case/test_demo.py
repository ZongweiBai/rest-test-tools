# coding:utf8
import os
import unittest

import requests

from core.main.run_group_test import RunGroupTest
from core.core_config import CoreConfig


class Demo(unittest.TestCase):

    def test_case01(self):
        respose = requests.get('http://www.baidu.com')
        print(respose.text)
        self.assertTrue(respose.status_code, '200')
        print('接口正常')

    def test_case02(self):
        # 获取当前文件的路径
        current_path = os.path.abspath(os.path.dirname(__file__))
        # 获取当前文件的上级路径
        parent_path = os.path.dirname(current_path)
        test_case_excel = os.path.join(parent_path, 'case/interface.xls')
        runtest = RunGroupTest(test_case_excel)
        runtest.go_on_run()

    def test_oauth_acl(self):
        core_config = CoreConfig()
        runtest = RunGroupTest(os.path.join(core_config.test_case_file_path, 'oauth_server_test.xls'), 0)
        runtest.go_on_run()
