# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/2/24 21:52
@file:permissions.py
@desc:
'''

from rest_framework import permissions
# 自定义权限类
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 如果是访问之类的http方法-通过
        if request.method in permissions.SAFE_METHODS:
            return True
        # 当前用户是否属于该项目管理员
        return obj.admin==request.user