# Create your views here.
from django.contrib import auth
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from httprunner.cli import main_run
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from sqtp.models import Request,Case,Step,Project,Environment,User
from sqtp.permissions import IsOwnerOrReadOnly
from sqtp.serializers import RequestSerializer, CaseSerializer, StepSerializer, ProjectSerializer, \
    EnvironmentSerializer, UserSerializer, RegisterSerializer, LoginSerializer


@api_view(['GET','POST'])
def request_list(request,format=None):
    if request.method=="GET":
        serializer=RequestSerializer(Request.objects.all(), many=True)
        # safe=False是为了支持{}以外的python对象转json
        return Response(serializer.data)
    elif request.method=="POST":
        serializer=RequestSerializer(data=request.data)
        # 判断数据是否合法
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# format=None 能够支持系统返回其他格式的数据，例如http://127.0.0.1:8000/sqtp/request.json
@api_view(['GET','PUT','DELETE'])
def request_detail(request,_id,format=None):
    try:
        res=Request.objects.get(id=_id)
    except Request.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=="GET":
        serializer=RequestSerializer(res)
        return Response(serializer.data)
    elif request.method=="PUT":
        serializer=RequestSerializer(res,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=="DELETE":
        res.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class RequestList(APIView):
#     def get(self,format=None):
#         serializer=RequestSerializer(Request.objects.all(), many=True)
#         # safe=False是为了支持{}以外的python对象转json
#         return Response(serializer.data)
#     def post(self,request):
#         serializer=RequestSerializer(data=request.data)
#         # 判断数据是否合法
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class RequestDetail(APIView):
#     def get_object(self,_id):
#         try:
#             res=Request.objects.get(id=_id)
#             return res
#         except Request.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def get(self,request,_id,format=None):
#         req_obj=self.get_object(_id)
#         if isinstance(req_obj,Response):
#             return req_obj
#         serializer=RequestSerializer(req_obj)
#         return Response(serializer.data)
#     def put(self,request,_id,format=None):
#         req_obj=self.get_object(_id)
#         serializer=RequestSerializer(req_obj,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,_id,format=None):
#         req_obj=self.get_object(_id)
#         req_obj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# 优化视图，使用通用类视图
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
class RequestList(ListCreateAPIView):
    '''
    查询所有数据和新增单个数据的功能
    '''
    queryset=Request.objects.all()
    serializer_class=RequestSerializer

class RequestDetail(RetrieveUpdateDestroyAPIView):
    queryset=Request.objects.all()
    serializer_class=RequestSerializer

# 继续优化：视图集--增删改查
@method_decorator(name="list",decorator=swagger_auto_schema(operation_summary="列出数据",operation_description="列出请求数据"))
@method_decorator(name="create",decorator=swagger_auto_schema(operation_summary="增加数据",operation_description="增加请求数据"))
@method_decorator(name="retrieve",decorator=swagger_auto_schema(operation_summary="查看详情",operation_description="查看单个请求数据"))
@method_decorator(name="destroy",decorator=swagger_auto_schema(operation_summary="删除数据",operation_description="删除请求数据"))
@method_decorator(name="update",decorator=swagger_auto_schema(operation_summary="更新数据",operation_description="更新请求数据"))
class RequestViewSet(ModelViewSet):
    queryset=Request.objects.all()
    serializer_class=RequestSerializer

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