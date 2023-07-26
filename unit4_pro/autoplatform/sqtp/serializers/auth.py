# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/3/2 13:43
@file:auth.py
@desc:
'''
from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from sqtp.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','date_joined','email','is_active','is_superuser','phone','realname','username','user_type']

# 注册序列器
class RegisterSerializer(serializers.ModelSerializer):
    # admin_code不在User字段中，需要新创建定义
    admin_code=serializers.CharField(default="sqtp")
    class Meta:
        model=User
        fields=['username', 'password', 'email', 'phone', 'realname', 'admin_code']

    # 校验入参是否合法
    def validate(self, attrs):
        if 'admin_code' in attrs and attrs['admin_code']!='sqtp':
            raise ValidationError('错误的admin_code')
        return attrs

    # 重写序列化器的保存方法
    def register(self):
        in_param=self.data
        if 'admin_code' in in_param:
            in_param.pop('admin_code')
            user=User.objects.create_superuser(**in_param) # 创建管理员
        else:
            user=User.objects.create_user(**in_param) # 创建普通用户
        return user

# 登录序列器
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']

    def validate(self, attrs):
        # 检查必填参数
        position_params=['username','password']
        for param in position_params:
            if param not in attrs:
                raise ValidationError(f'缺少参数：{param}')
        # 验证用户名密码
        user=auth.authenticate(**attrs)
        if not user:
            raise ValidationError("用户名或密码不正确")
        return user