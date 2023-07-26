# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/7/5 0:17
@file:hr3.py
@desc:
'''
import os
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from httprunner.cli import main_run
from httprunner import loader,compat
from sqtp.models import Case,Step,Request
from sqtp.serializers import CaseSerializer,StepSerializer,RequestSerializer


class CaseViewSet(ModelViewSet):
    queryset=Case.objects.all()
    serializer_class=CaseSerializer
    # 创建及更新用户
    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(methods=['GET'],detail=True,url_path='run',url_name='run_case')
    # 完整的url等于/cases/<int:case_id>/run
    def run_case(self,request,pk):
        case=Case.objects.get(pk=pk)
        serializer=self.get_serializer(instance=case)
        # 生成用例文件
        path=serializer.to_json_file()
        # hr3运行测试用例
        exit_code=main_run([path])
        if exit_code!=0:
            return Response(data={'error':'failed run case','retcode':exit_code},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={'msg':' run success','retcode':status.HTTP_200_OK})

class StepViewSet(ModelViewSet):
    queryset=Step.objects.all()
    serializer_class=StepSerializer

# 继续优化：视图集--增删改查
@method_decorator(name="list",decorator=swagger_auto_schema(operation_summary="列出数据",operation_description="列出请求数据"))
@method_decorator(name="create",decorator=swagger_auto_schema(operation_summary="增加数据",operation_description="增加请求数据"))
@method_decorator(name="retrieve",decorator=swagger_auto_schema(operation_summary="查看详情",operation_description="查看单个请求数据"))
@method_decorator(name="destroy",decorator=swagger_auto_schema(operation_summary="删除数据",operation_description="删除请求数据"))
@method_decorator(name="update",decorator=swagger_auto_schema(operation_summary="更新数据",operation_description="更新请求数据"))
class RequestViewSet(ModelViewSet):
    queryset=Request.objects.all()
    serializer_class=RequestSerializer

class FileUploadView(APIView):
    # 指定数据解析器
    parser_classes=[FileUploadParser,]

    def put(self,request,filename,format=None):
        # 接收文件
        file_obj=request.data['file']
        if not os.path.exists('upload'):
            os.makedirs('upload')
        with open(f'upload/{filename}','wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        # 去除前三行和最后1行
        with open(f'upload/{filename}',) as f:
            lines=f.readlines()[3:][:-1]
        with open(f'upload/{filename}','w') as f:
            for line in lines:
                f.write(line)
        # 检查文件内容
        try:
            content=loader.load_test_file(f'upload/{filename}')
            valida_case=compat.ensure_testcase_v4(content)
        except Exception as e:
            raise serializers.ValidationError(f'错误的hr3用例格式: {repr(e)}')

        # 内容导入到数据库
        serializer=CaseSerializer(data=valida_case)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(status=400,data={'retcode':400,'msg':'upload failed','error':serializer.errors})
        return Response(status=204,data={'retcode':204,'msg':f'{filename} uploaded'})