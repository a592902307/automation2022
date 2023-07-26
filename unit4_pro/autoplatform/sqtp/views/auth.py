# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/7/5 0:11
@file:auth.py
@desc:
'''
from django.contrib import auth
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from sqtp.models import User
from sqtp.serializers import UserSerializer,LoginSerializer,RegisterSerializer

# 用户视图
@api_view(['GET'])
# 全局认证模块，及权限模块（IsAuthenticated：判断是否登录）
@authentication_classes((BasicAuthentication,SessionAuthentication))
@permission_classes((IsAuthenticated,))
def user_list(request):
    queryset=User.objects.all()
    serializer=UserSerializer(queryset,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user_detail(request,_id):
    try:
        req_obj=User.objects.get(pk=_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer=UserSerializer(req_obj)
    return Response(serializer.data)

# 注册视图
@api_view(['POST'])
@permission_classes(())
def register(request):
    serializer=RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.register()
        auth.login(request,user)
        return Response(status=status.HTTP_201_CREATED,data={"msg":"register success","is_admin":user.is_superuser,"retcode":status.HTTP_201_CREATED})
    return Response(status=status.HTTP_400_BAD_REQUEST,data={"msg":"error","retcode":status.HTTP_400_BAD_REQUEST,"error":serializer.errors})
# 登录视图
@api_view(['POST'])
@permission_classes(())
def login(request):
    serializer=LoginSerializer(data=request.data)
    user=serializer.validate(request.data)
    if user:
        auth.login(request,user)
        return Response(status=status.HTTP_302_FOUND,data={"msg":"login success","to":"index.html"})
    Response(status=status.HTTP_400_BAD_REQUEST,
             data={"msg":"error","retcode":status.HTTP_400_BAD_REQUEST,"error":serializer.errors})
# 登出视图
@api_view(['GET'])
def logout(request):
    # 当前用户是否为登录状态，是的话登出
    if request.user.is_authenticated:
        auth.logout(request)
    return Response(status=status.HTTP_302_FOUND,data={"msg":"logout success","to":"login.html"})
# 获取当前用户登录信息
@api_view(['GET'])
@permission_classes(())
def current_user(request):
    if request.user.is_authenticated:
        serializer=UserSerializer(request.user)
        return Response(data=serializer.data)
    else:
        return Response(status=403,data={"msg":"未登录","retcode":403,"to":"login.html"})
