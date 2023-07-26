# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/7/5 21:42
@file:mgr.py
@desc:
'''
from rest_framework.viewsets import ModelViewSet
from sqtp.permissions import IsOwnerOrReadOnly
from sqtp.models import Project,Environment
from sqtp.serializers import ProjectSerializer,EnvironmentSerializer

class ProjectViewSet(ModelViewSet):
    queryset=Project.objects.all()
    serializer_class=ProjectSerializer
    # 视图应用权限
    permission_classes=(IsOwnerOrReadOnly,)

class EnvironmentViewSet(ModelViewSet):
    queryset=Environment.objects.all()
    serializer_class=EnvironmentSerializer
    # 权限，传空表明不去做权限认证
    permission_classes=(())