# coding:utf-8
import os


class CoreConfig:
    """
    全局变量
    """

    def __init__(self):
        # core目录所在的绝对路径
        self.core_path = os.path.abspath(os.path.dirname(__file__))
        # 项目根目录所在的绝对路径
        self.project_path = os.path.dirname(self.core_path)
        # 测试用例所在的绝对路径
        self.test_case_path = os.path.join(self.project_path, 'test_case')
        # 测试用例文件定义所在的绝对路径
        self.test_case_file_path = os.path.join(self.project_path, 'case')
        # 测试用例配置所在的绝对路径
        self.data_config_path = os.path.join(self.project_path, 'dataconfig')
        # 日志文件所在的绝对路径
        self.log_path = os.path.join(self.project_path, 'log')
        # 测试报告所在的绝对路径
        self.report_path = os.path.join(self.project_path, 'test_report')
