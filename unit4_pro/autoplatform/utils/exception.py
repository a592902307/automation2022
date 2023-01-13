# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2022/12/27 22:07
@file:exception.py
@desc:
'''
from requests import exceptions
from rest_framework.views import exception_handler,Response

# 处理异常返回
def my_exception_handler(exc,context):
    '''
    先调用默认的异常处理获取标准错误响应
    exc:异常信息
    context：上下文
    '''
    error_response=exception_handler(exc,context)
    if error_response:
        if isinstance(error_response,exceptions.RequestException):
            error_msg=exc.detail
        else:
            # 异常为Http404或者PermissionDenied
            error_msg=exc

        error_response.data={
            'msg':'error',
            'retcode':error_response.status_code,
            'error':str(error_msg)
        }
    return error_response