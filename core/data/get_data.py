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

    # 解析excel的数据并返回
    def parse_excel_file(self):
        return self.oper_excel.parse_excel_file()

    # 写入数据
    def write_result(self, row, value):
        col = int(data_config.get_result())
        self.oper_excel.write_value(row, col, value)

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

        request_params = {}
        if excel_data.request_param is not None and excel_data.request_param != '':
            request_params = json.loads(excel_data.request_param)

        request_body = None
        if excel_data.request_body is not None and excel_data.request_body != '':
            request_body = json.loads(excel_data.request_body)

        '''
        判断是否有依赖的case，如果有，从响应中获取数据并组装新的请求信息
        '''
        if excel_data.dependent_case_id is not None and excel_data.dependent_case_id != '' \
                and excel_data.dependent_field is not None and excel_data.dependent_field != '':

            # 获取依赖字段的响应数据
            depend_response_data = dependent_data.get_dependent_data(excel_data.dependent_case_id,
                                                                     excel_data.dependent_key)
            # 将依赖case的响应返回中某个字段的value赋值给该接口请求中某个参数
            dependent_field_length = len(excel_data.dependent_field)
            if "param:" in excel_data.dependent_field:
                dependent_field = excel_data.dependent_field[len("param:"), dependent_field_length]
                request_params[dependent_field] = depend_response_data
            elif "body:" in excel_data.dependent_field:
                dependent_field = excel_data.dependent_field[len("body:"), dependent_field_length]
                request_body[dependent_field] = depend_response_data
            elif "header:" in excel_data.dependent_field:
                request_header_field = excel_data.dependent_field[len("header:"):dependent_field_length]
                if "Authorization" in excel_data.dependent_field:
                    request_header[request_header_field] = 'Bearer ' + depend_response_data
                else:
                    request_header[request_header_field] = depend_response_data

        return request_params, request_body, request_header
