# coding=utf-8

import os
import unittest

from core.extension.HTMLTestRunner import HTMLTestRunner

# 当前文件路径
current_path = os.getcwd()
# 获取当前文件的上级路径
parent_path = os.path.dirname(current_path)
# 测试用例的路径
test_case_path = os.path.join(parent_path, 'test_case')
# 测试报告的存放路径
test_report_path = os.path.join(parent_path, 'test_report')


# 找出以test开头的用例
def discovery_test_case():
    discover = unittest.defaultTestLoader.discover(test_case_path, pattern='test*.py')
    return discover


if __name__ == '__main__':
    report_path_exists = os.path.exists(test_report_path)
    if not report_path_exists:
        os.mkdir(test_report_path)

    # 测试报告为test_report.html
    test_report_path = os.path.join(test_report_path, 'test_report.html')

    # 打开文件，把结果写入到文件，有内容的话，先清空再写
    fp = open(test_report_path, 'wb')

    runner = HTMLTestRunner(stream=fp, title='Python Test Tools测试报告', description='测试用例测试情况')

    # 调用discovery_test_case函数返回值
    runner.run(discovery_test_case())

    # 关闭刚才打开的文件
    fp.close()
