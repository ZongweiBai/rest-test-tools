# coding:utf-8
from jsonpath_rw import parse

from core.data.get_data import GetData
from core.util.operation_excel import OperationExcel
from core.util.request_http import RequestHttp


class DependentData:
    """解析依赖case"""

    def __init__(self):
        self.__data_cache = {}
        self.oper_excel = OperationExcel()
        self.method = RequestHttp()
        self.data = GetData()

    def put_cache(self, case_id, response):
        """
        将请求结果放入缓存
        :param case_id:  测试用例ID
        :param response: 测试用例的响应信息
        :return:
        """
        self.__data_cache[case_id] = response
        print(self.__data_cache)

    def get_dependent_data(self, depend_case_id, depend_key):
        """
        从缓存中获取指定表达式的值
        :param depend_case_id:  依赖的测试用例ID
        :param depend_key:      指定字段或表达式
        :return:
        """
        response_data = self.__data_cache[depend_case_id]
        return [match.value for match in parse(depend_key).find(response_data)][0]
