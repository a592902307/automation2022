from django.db.models import Value
from django.test import TestCase

# Create your tests here.
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from sqtp.models import Config,Case,Step,Request
from sqtp.serializers import RequestSerializer
import io

class TestRelatedQuery(TestCase):
    def setUp(self) -> None:
        config1=Config.objects.create(name="case001",base_url="http://localhost")
        config2=Config.objects.create(name="case002",base_url="http://localhost")
        self.case1=Case.objects.create(config=config1)
        self.case2=Case.objects.create(config=config2)

    def test_steps_query(self):
        step1=Step.objects.create(belong_case=self.case1,name='step1')
        step1.linked_case=self.case2
        step1.save()
        step2=Step.objects.create(belong_case=self.case2,name='step2')

        # 正向查询:有外键的模型查询被关联的模型
        print('=============正向查询============')
        print(step1.belong_case)
        print(step1.linked_case)
        # 反向查询：无外键的模型查询有外键的模型
        print('=============反向查询============')
        # related_name代替step_set
        print(self.case1.teststeps.all())
        print(self.case2.linked_steps.all())

class TestJsonField(TestCase):
    def setUp(self) -> None:
        req1=Request.objects.create(method=1,url='/mgr/course/',data={"name":"小明","age":16,"address":"nanjing"})
        req2=Request.objects.create(method=2,url='/mgr/teacher/',data={"name":"小王","age":18,"address":"hangzhou"})
    def test_json1(self):
        req=Request.objects.all().first()
        print(req)
        req.data={"name":"小白","age":18,"address":"shanghai","school":{"name":"beijinguniversity","level":"top1"}}
        req.save()
        print(Request.objects.all().first().data)

        # 修改局部
        req.data["name"]="星辰大海"
        req.save()
        print(Request.objects.all().first().data)

        # 删除部分
        req.data.pop("age")
        req.save()
        print(Request.objects.all().first().data)

        # 删除全部
        # req.data=Value('null') # 设置成json的null
        # req.data=None # 设置成sql的null
        # req.save()
        # print(Request.objects.all().first().data)

        # 条件查询--根据json字段的某个值来查询，json字段__嵌套字段
        # res=Request.objects.filter(data__age=18)
        # res=Request.objects.filter(data__school__name="beijinguniversity")
        # res=Request.objects.filter(url__contains="teacher")
        # res=Request.objects.filter(data__name__exact="小")
        res=Request.objects.filter(data__address__in=["shanghai","hangzhou"])
        print('======json条件查询=====')
        print(res)

class TestRequestSerializer(TestCase):
    req1=Request.objects.create(url='/demo1',data={'name':'小明','age':18,'addr':'nanjing'})
    req2=Request.objects.create(url='/demo1',params={'name':'小明','age':18,'addr':'nanjing'})
    # 序列化
    req_ser=RequestSerializer(req1)
    print(req_ser.data)
    content=JSONRenderer().render(req_ser.data)
    print(content)

    # 反序列化：steam流转化成python原生数据类型
    stream=io.BytesIO(content)
    data=JSONParser().parse(stream)
    # python原生数据类型转化成django对象实例
    ser=RequestSerializer(data=data)
    print(ser.is_valid()) # 校验数据合法
    print(ser.validated_data) # 查看数据对象
    ser.save()

    print(repr(ser))
