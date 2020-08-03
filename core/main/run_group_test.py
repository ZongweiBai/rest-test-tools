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
from core.util.log_printer import Logger
from core.core_config import CoreConfig


class RunGroupTest:
    """运行组测试"""

    def __init__(self, file_name=None, sheet_id=0):
        self.core_config = CoreConfig()
        self.logger = Logger(use_console=False).logger
        self.request_http = RequestHttp()
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

        excel_data_list = self.data.parse_excel_file()

        index = 1
        for excel_data in iter(excel_data_list):
            try:
                if excel_data.run_test_case:

                    request_info = self.data.refresh_request_info(excel_data, self.dependent_data)
                    res = self.request_http.execute(excel_data.request_method, excel_data.request_url,
                                                    request_info[0], request_info[1], request_info[2])

                    if excel_data.expect_http_code != res.status_code:
                        fail_count.append(index)
                        self.logger.error(("第%s条用例报错:" % index))
                        self.logger.exception("第%s条用例Http状态码响应结果与预期结果不一致" % index)
                        raise Exception("第%s条用例Http状态码响应结果与预期结果不一致" % index)

                    # excel中拿到的expect数据是str类型，但是返回的res是dict类型，两者数据比较必须都是字符类型
                    if self.com_util.is_contain(excel_data.expect_http_response, json.dumps(res.json())):
                        self.data.write_result(index, 'pass')
                        pass_count.append(index)

                        # 将响应放入缓存中
                        self.dependent_data.put_cache(excel_data.test_case_id, res.json())
                    else:
                        # 返回的res是dict类型，要将res数据写入excel中，需将dict类型转换成str类型
                        self.data.write_result(index, json.dumps(res.json()))
                        fail_count.append(index)
                        self.logger.error(("第%s条用例实际响应结果:%s" % index, res.json()))
                        self.logger.exception("第%s条用例实际结果与预期结果不一致" % index)
                        raise Exception("第%s条用例实际结果与预期结果不一致" % index)
                else:
                    no_run_count.append(index)
            except Exception as e:
                # 将异常写入excel的测试结果中
                self.data.write_result(index, str(e))
                # 将报错写入指定路径的日志文件里
                self.logger.error(("第%s条用例报错:" % index))
                self.logger.exception(e)
                fail_count.append(index)
                # 手动抛出异常
                raise Exception(print(e))

            index = index + 1
        # self.send_mail.send_main(pass_count,fail_count,no_run_count)


# 当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行
if __name__ == '__main__':
    run = RunGroupTest()
    run.go_on_run()
