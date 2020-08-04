# coding:utf-8

class global_var():
    # case_id
    result = '13'

# 获取result
def get_result():
    return global_var.result
