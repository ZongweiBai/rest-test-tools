# coding:utf-8


class ExcelData:
    """excel字段定义"""

    # 测试用例ID
    test_case_id = None

    # 测试用例名称
    test_case_name = None

    # 该条测试用例是否运行
    run_test_case = 'yes'

    # 请求url
    request_url = None

    # 请求方法 get|post|delete|put
    request_method = 'get'

    # 请求头
    request_header = None

    # 请求参数
    request_param = None

    # 请求body
    request_body = None

    # 依赖的测试用例ID
    dependent_case_id = None

    # 依赖返回的哪些数据
    dependent_key = None

    # 哪些字段依赖返回的数据
    dependent_field = None

    # 期望的Http状态码
    expect_http_code = 200

    # 期望的响应
    expect_http_response = None
