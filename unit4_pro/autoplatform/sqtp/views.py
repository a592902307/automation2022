from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from sqtp.models import Request,Case,Step
from sqtp.serializers import RequestSerializer,CaseSerializer,StepSerializer

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

class StepViewSet(ModelViewSet):
    queryset=Step.objects.all()
    serializer_class=StepSerializer