# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2022/12/21 14:48
@file:test_serializers.py
@desc:
'''

from django.test import TestCase
from sqtp.models import Step,Request
from sqtp.serializers import RequestSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

class TestRequestSerializer(TestCase):
    req1 = Request.objects.create(method=1, url='/demo1', data={"name": "小明", "age": 16, "address": "nanjing"})
    req2 = Request.objects.create(method=2, url='/demo2', data={"name": "小王", "age": 18, "address": "hangzhou"})
    # 序列化：数据对象-->>python原生数据类型（字典）
    req1_serializer=RequestSerializer(req1)
    print(req1_serializer.data) # 从序列化对象中提取序列化数据（存在data中）
    # 序列化: python原生数据类型-->>json
    content=JSONRenderer().render(req1_serializer.data)
    print(content)
    print(type(content))

    # 返序列化：1、构建stream流，转成python原生数据类型（字典）
    steam=io.BytesIO(content)
    data=JSONParser().parse(steam)
    # 2、python原生数据类型（字典）-->>正常的对象实例
    serializer=RequestSerializer(data=data)
    # 校验数据是否合法
    if serializer.is_valid():
        print(serializer.validated_data)  # 校验之后的数据会放在validated_data中
        serializer.save()

    # 序列化器查看结果集
    serializer=RequestSerializer(Request.objects.all(),many=True)
    print(serializer.data)

    # 序列化内部源码
    print(repr(serializer))