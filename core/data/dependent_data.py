# coding:utf-8
from jsonpath_rw import parse

from core.data.get_data import GetData
from core.util.operation_excel import OperationExcel
from core.util.request_http import RequestHttp


class DependentData:

    def __init__(self):
        self.__data_cache = {}
        self.oper_excel = OperationExcel()
        self.method = RequestHttp()
        self.data = GetData()

    # 通过case_id去获取依赖case_id的整行数据
    def get_case_line_data(self):
        import warnings
        warnings.warn("已过时", DeprecationWarning)
        rows_data = self.oper_excel.get_rows_data(self.case_id)
        return rows_data

    # 执行依赖测试，获取结果
    def run_dependent(self):
        import warnings
        warnings.warn("已过时", DeprecationWarning)
        row_num = self.oper_excel.get_row_num(self.case_id)
        request_data = self.data.get_data_value(row_num)
        header = self.data.get_request_header(row_num)
        method = self.data.get_request_method(row_num)
        url = self.data.get_request_url(row_num)
        res = self.method.execute(method, url, request_data, header, params=request_data)
        return res

    # 获取依赖字段的响应数据：通过执行依赖测试case来获取响应数据，响应中某个字段数据作为依赖key的value
    def get_value_for_key(self, row):
        import warnings
        warnings.warn("已过时", DeprecationWarning)
        # 获取依赖的返回数据key
        depend_data = self.data.get_depend_key(row)
        # 执行依赖case返回结果
        response_data = self.run_dependent()
        # print(depend_data)
        # print(response_data)

        return [match.value for match in parse(depend_data).find(response_data)][0]

    # 将请求结果放入缓存
    def put_cache(self, case_id, response):
        self.__data_cache[case_id] = response
        print(self.__data_cache)

    def get_dependent_data(self, depend_case_id, depend_field):
        response_data = self.__data_cache[depend_case_id]
        return [match.value for match in parse(depend_field).find(response_data)][0]
