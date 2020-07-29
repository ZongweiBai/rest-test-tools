# coding:utf-8

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from core.util.request_http import RequestHttp
from core.data.get_data import GetData
from core.util.common_assert import CommonUtil
import json
from core.data.dependent_data import DependentData
from core.util.send_mail import SendEmail
from core.util.operation_header import OperationHeader
from core.util.operation_json import OperationJson
from core.util.log_printer import Logger
from core.core_config import CoreConfig


class RunGroupTest:

    def __init__(self, file_name=None, sheet_id=0):
        self.core_config = CoreConfig()
        self.logger = Logger(use_console=False).logger
        self.run_method = RequestHttp()
        self.data = GetData(file_name=file_name, sheet_id=sheet_id)
        self.com_util = CommonUtil()
        self.send_mail = SendEmail()
        self.dependent_data = DependentData()

    # 程序执行
    def go_on_run(self):
        res = None
        pass_count = []
        fail_count = []
        no_run_count = []
        rows_count = self.data.get_case_lines()

        for index in range(1, rows_count):
            try:
                is_run = self.data.get_is_run(index)
                if not is_run:
                    no_run_count.append(index)
                    continue

                case_id = self.data.get_request_id(index)
                url = self.data.get_request_url(index)
                method = self.data.get_request_method(index)
                # 获取请求参数
                data = self.data.get_data_value(index)
                # 获取excel文件中header关键字
                header_key = self.data.get_request_header(index)
                # 获取json文件中header_key对应的头文件数据
                header = self.data.get_header_value(index)
                expect = self.data.get_expect_data(index)
                depend_case_id = self.data.is_depend(index)
                depend_key = self.data.get_depend_key(index)
                depend_field = self.data.get_depend_field(index)

                if depend_case_id is not None:
                    # 获取依赖字段的响应数据
                    depend_response_data = self.dependent_data.get_dependent_data(depend_case_id, depend_key)
                    # 将依赖case的响应返回中某个字段的value赋值给该接口请求中某个参数
                    data[depend_field] = depend_response_data

                # cookie相关的没有跑通，代码逻辑是正常的，但是模拟登陆返回一直是非法请求
                if header_key == 'write_Cookies':
                    res = self.run_method.execute(method, url, data, header, params=data)
                    op_header = OperationHeader(res)
                    op_header.write_cookie()

                elif header_key == 'get_Cookies':
                    op_json = OperationJson(os.path.join(self.core_config.data_config_path, 'cookie.json'))
                    cookie = op_json.get_data('apsid')
                    cookies = {'apsid': cookie}
                    res = self.run_method.execute(method, url, data, header=cookies, params=data)

                else:
                    res = self.run_method.execute(method, url, data, header, params=data)

                '''
                get请求参数是params:request.get(url='',params={}),post请求数据是data:request.post(url='',data={})
                excel文件中没有区分直接用请求数据表示,则data = self.data.get_data_value(i)拿到的数据，post请求就是data=data,get请求就是params=data
                '''

                # excel中拿到的expect数据是str类型，但是返回的res是dict类型，两者数据比较必须都是字符类型
                if self.com_util.is_contain(expect, json.dumps(res)):
                    self.data.write_result(index, 'pass')
                    pass_count.append(index)

                    # 将响应放入缓存中
                    self.dependent_data.put_cache(case_id, res)
                else:
                    # 返回的res是dict类型，要将res数据写入excel中，需将dict类型转换成str类型
                    self.data.write_result(index, json.dumps(res))
                    # with open(log_file, 'a', encoding='utf-8') as f:
                    #     f.write("\n第%s条用例实际结果与预期结果不一致:\n" % i)
                    #     f.write("Expected:%s\n  Actual:%s\n" % (expect, res))
                    fail_count.append(index)
                    self.logger.error(("第%s条用例报错:" % index))
                    self.logger.exception("第%s条用例实际结果与预期结果不一致" % index)
                    # raise Exception("第%s条用例实际结果与预期结果不一致" % index)

            except Exception as e:
                # 将异常写入excel的测试结果中
                self.data.write_result(index, str(e))
                # 将报错写入指定路径的日志文件里
                self.logger.error(("第%s条用例报错:" % index))
                self.logger.exception(e)
                fail_count.append(index)
                # 手动抛出异常
                raise Exception(print(e))

        # self.send_mail.send_main(pass_count,fail_count,no_run_count)


# 当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行
if __name__ == '__main__':
    run = RunGroupTest()
    run.go_on_run()
