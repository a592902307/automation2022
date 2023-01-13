# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2022/12/21 13:30
@file:serializers.py
@desc:
'''

from rest_framework import serializers
from sqtp.models import Step,Request,Config,Case

# 设置序列化器：命名规范：模型名+Serializer
class RequestSerializer(serializers.ModelSerializer):
    # 会自动调用get_method方法，赋值给method
    method=serializers.SerializerMethodField()
    def get_method(self,obj):
        # 返回choice的 displayname而不是实际值
        return obj.get_method_display()
    class Meta:
        model=Request
        # 指定序列化模型中的字段
        fields="__all__"
        # fields =['step','method','url','params','headers']

# 配置
class ConfigSerializer(serializers.ModelSerializer):
   class Meta:
       model=Config
       fields='__all__'
# 用例
class CaseSerializer(serializers.ModelSerializer):
   # config=ConfigSerializer(read_only=True) # config字段为Config序列化器，REST会自动提取其值
   class Meta:
       model=Case
       fields='__all__'

# 测试步骤
class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model=Step
        fields='__all__'
