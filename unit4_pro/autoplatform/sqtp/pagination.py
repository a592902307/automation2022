# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/7/13 17:12
@file:pagination.py
@desc:
'''

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MyPageNumberPagination(PageNumberPagination):
    # 默认返回的size
    page_size=5
    page_size_query_param='page_size'
    page_query_param='page_index'

    # 覆盖返回的数据格式
    def get_paginated_response(self,data):
        resp_data={
            'retlist':data,
            'total':self.page.paginator.count
        }
        return Response(resp_data)