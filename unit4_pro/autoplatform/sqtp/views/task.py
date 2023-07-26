# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/7/5 21:44
@file:task.py
@desc:
'''
import subprocess
import uuid
from httprunner.cli import main_run
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from sqtp.models import Plan,Report
from sqtp.serializers import PlanSerializer,CaseSerializer,ReportSerializer
from sqtp.utils import setup_case_dir,setup_logs_dir,collect_log
from sqtp.pagination import MyPageNumberPagination


class PlanViewSet(ModelViewSet):
    queryset=Plan.objects.all()
    serializer_class=PlanSerializer
    # 同步创建者
    def perform_create(self,serializer):
        serializer.save(create_by=self.request.user)

    # 同步更新者
    def perform_update(self,serializer):
        serializer.save(updated_by=self.request.user)

    # 定义运行测试计划方法
    @action(methods=['GET'],detail=True,url_path='run',url_name='run_plan')
    def run(self,request,pk):
        # 获取测试计划，更新测试状态
        plan=Plan.objects.get(pk=pk)
        plan.status=1
        plan.save()
        # 初始化用例目录，清空用例目录，清空日志目录
        setup_case_dir('testcase')
        setup_logs_dir('logs')

        case_list=[]
        # 取出计划关联的用例，序列化，然后生成用例文件加入用例列表中
        for case in plan.cases.all():
            serializer=CaseSerializer(instance=case)
            path=serializer.to_json_file()
            case_list.append(path)

        # 报告路径采取uuid随机值
        allure_path=f'report/{uuid.uuid4()}'
        # hr3批量运行用例
        # exit_code=main_run([*case_list,'--alluredir=report/tmp'])
        exit_code = main_run([*case_list,f'--alluredir={allure_path}'])
        # 生成allure报告文件，--报告文件储存到静态文件目录下
        subprocess.Popen(f'allure generate {allure_path} -o dist/{allure_path}',shell=True)
        # 从log中获取报告详情，保存报告内容到数据库
        detail=collect_log('logs')
        Report.objects.create(plan=plan,path=f'{allure_path}/index.html',trigger=request.user,detail=detail)
        # 更新测试计划状态及执行次数
        plan.exec_counts=plan.exec_counts+1
        plan.status=3
        plan.save()

        # 只要exit_code不是0，就是执行失败了
        if exit_code != 0:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,data={'error':'failed run plan','retcode':exit_code})
        return Response(status=status.HTTP_200_OK,data={'retcode':status.HTTP_200_OK,'msg':'run success'})

# ReadOnlyModelViewSet表示该视图只提供查询功能
class ReportViewSet(ReadOnlyModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    # 可以不定义全局分页器，然后局部视图使用自定义分页器
    pagination_class = MyPageNumberPagination

    # def create(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_404_NOT_FOUND,data={'retcode':404,'msg':'no such method'})
    # def update(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_404_NOT_FOUND,data={'retcode':404,'msg':'no such method'})