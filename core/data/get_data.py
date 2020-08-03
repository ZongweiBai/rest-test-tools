# coding:utf-8
import json
import os

from core.core_config import CoreConfig
from core.data import data_config
from core.util.operation_excel import OperationExcel
from core.util.operation_json import OperationJson


class GetData:
    def __init__(self, file_name=None, sheet_id=0):
        self.core_config = CoreConfig()
        # 当前文件路径
        self.current_path = os.path.abspath(os.path.dirname(__file__))
        # 获取当前文件的上级路径
        self.parent_path = os.path.dirname(self.current_path)
        self.parent_path = os.path.dirname(self.parent_path)
        self.oper_excel = OperationExcel(file_name=file_name, sheet_id=sheet_id)

    # 去获取excel行数，就是case个数
    def get_case_lines(self):
        return self.oper_excel.get_lines()

    # 解析excel的数据并返回
    def parse_excel_file(self):
        return self.oper_excel.parse_excel_file()

    # 获取是否执行
    def get_is_run(self, row):
        flag = None
        col = int(data_config.get_run())
        run_model = self.oper_excel.get_cell_value(row, col)
        if run_model == 'yes':
            flag = True
        else:
            flag = False
        return flag

    # 获取请求方式
    def get_request_method(self, row):
        col = int(data_config.get_request_way())
        request_method = self.oper_excel.get_cell_value(row, col)
        return request_method

    # 获取url
    def get_request_url(self, row):
        col = int(data_config.get_url())
        url = self.oper_excel.get_cell_value(row, col)
        return url

    # 获取请求头header
    def get_request_header(self, row):
        col = int(data_config.get_header())
        data = self.oper_excel.get_cell_value(row, col)
        if data == '':
            return None
        else:
            return data

    # 通过获取头关键字拿到data数据
    def get_header_value(self, row):
        request_header_file = os.path.join(self.parent_path, 'dataconfig/request_header.json')
        oper_json = OperationJson(request_header_file)
        request_header = oper_json.get_data(self.get_request_header(row))
        return request_header

    # 获取请求数据
    def get_request_data(self, row):
        col = int(data_config.get_data())
        data = self.oper_excel.get_cell_value(row, col)
        if data == '':
            return None
        return data

    # 通过获取请求关键字拿到data数据
    def get_data_value(self, row):
        request_data_file = os.path.join(self.parent_path, 'dataconfig/request_data.json')
        oper_json = OperationJson(request_data_file)
        request_data = oper_json.get_data(self.get_request_data(row))
        return request_data

    # 获取预期结果
    def get_expect_data(self, row):
        col = int(data_config.get_expect())
        expect = self.oper_excel.get_cell_value(row, col)
        return expect

    # 写入数据
    def write_result(self, row, value):
        col = int(data_config.get_result())
        self.oper_excel.write_value(row, col, value)

    # 获取依赖数据的key
    def get_depend_key(self, row):
        col = int(data_config.get_data_depend())
        depend_key = self.oper_excel.get_cell_value(row, col)
        if depend_key == '':
            return None
        else:
            return depend_key

    # 判断是否有case依赖
    def is_depend(self, row):
        col = int(data_config.get_case_depend())
        depend_case_id = self.oper_excel.get_cell_value(row, col)
        if depend_case_id == '':
            return None
        else:
            return depend_case_id

    # 获取请求依赖字段
    def get_depend_field(self, row):
        col = int(data_config.get_field_depend())
        data = self.oper_excel.get_cell_value(row, col)
        if data == '':
            return None
        else:
            return data

    def refresh_request_info(self, excel_data, dependent_data):
        """
        根据excel_data信息组装和获取完整的请求信息
        :param dependent_data:  DependentData的实例
        :param excel_data: excel的一行数据
        :return: 请求参数，请求body，请求header
        """

        '''
        合并公共请求header以及自定义请求header
        '''
        request_header = OperationJson(
            os.path.join(self.core_config.data_config_path, 'common_header.json')).read_data()
        if excel_data.request_header is not None:
            file_header_dict = json.loads(excel_data.request_header)
            request_header.update(file_header_dict)

        request_params = excel_data.request_param
        request_body = excel_data.request_body

        '''
        判断是否有依赖的case，如果有，从响应中获取数据并组装新的请求信息
        '''
        if excel_data.dependent_case_id is not None and excel_data.dependent_field is not None:

            # 获取依赖字段的响应数据
            depend_response_data = dependent_data.get_dependent_data(excel_data.dependent_case_id,
                                                                     excel_data.dependent_key)
            # 将依赖case的响应返回中某个字段的value赋值给该接口请求中某个参数
            dependent_field_length = len(excel_data.dependent_field)
            if "param:" in excel_data.dependent_field:
                request_params[len("param:"), dependent_field_length] = depend_response_data
            elif "body:" in excel_data.dependent_field:
                request_body[len("body:"), dependent_field_length] = depend_response_data
            elif "header:" in excel_data.dependent_field:
                if "Authorization" in excel_data.dependent_field:
                    request_header[len("header:"), dependent_field_length] = 'Bearer ' + depend_response_data
                else:
                    request_header[len("header:"), dependent_field_length] = depend_response_data

        return request_params, request_body, request_header
