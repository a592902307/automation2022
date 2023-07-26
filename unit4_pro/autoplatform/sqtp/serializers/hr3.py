# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/3/2 13:49
@file:hr3.py
@desc:
'''
from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer

from sqtp.models import Step, Request, Config, Case, Project
from sqtp.serializers import UserSerializer
from sqtp.serializers.mgr import ProjectSerializer

# 设置序列化器：命名规范：模型名+Serialize
from sqtp.utils import filter_data


class RequestSerializer(serializers.ModelSerializer):
    step_id=serializers.IntegerField(write_only=True,required=False)
    # 会自动调用get_method方法，赋值给method
    method=serializers.SerializerMethodField()
    def get_method(self,obj):
        # 返回choice的 displayname而不是实际值
        return obj.get_method_display()

    class Meta:
        model=Request
        # 指定序列化模型中的字段
        fields =['step_id','method','url','params','headers','json','data']

    def validate(self, attrs):
        template={
            'params':dict,
            'headers':dict,
            'cookies':dict
        }
        for key,value in template.items():
            if key in attrs and not isinstance(attrs[key],value):
                raise ValidationError(f'请传递正确的{key}格式：{value}')
        return attrs

# 配置
class ConfigSerializer(serializers.ModelSerializer):
    project=ProjectSerializer(required=False, read_only=True)
    class Meta:
        model=Config
        fields=['project','name','base_url','variables','parameters','export','verify']

    # 自定义过滤器来校验数据：无法估计前端传入什么类型的数据，需要自定义规则来验证
    def validate(self, attrs):
        if 'variables' in attrs and not isinstance(attrs['variables'],dict):
            raise ValidationError('请传递正确的variables格式：dict')
        if 'parameters' in attrs and not isinstance(attrs['parameters'],dict):
            raise ValidationError('请传递正确的parameters格式：dict')
        if 'export' in attrs and not isinstance(attrs['export'],list):
            raise ValidationError('请传递正确的export格式：list')
        if 'base_url' in attrs and not attrs['base_url'].startswith('http'):
            raise ValidationError('请传递正确的url：以http开头')
        return attrs

# 测试步骤
class StepSerializer(serializers.ModelSerializer):
    request=RequestSerializer()
    belong_case_id=serializers.IntegerField(required=False)

    def create(self, validated_data):
        req_kws=validated_data.pop('request')
        # 构造步骤
        step_obj=Step.objects.create(**validated_data)
        # 构造请求，请求关联step_id
        req_kws['step_id']=step_obj.id
        req_serializer=RequestSerializer(data=req_kws)
        if req_serializer.is_valid(raise_exception=True):
            req_obj=req_serializer.save()
        # else:
        #     raise ValidationError(req_serializer.errors)

        return step_obj

    class Meta:
        model=Step
        fields=['name','variables','request','extract','validate','setup_hooks','teardown_hooks','belong_case_id','sorted_no']

    def validate(self, attrs):
        template={
            'variables':dict,
            'request':dict,
            'extract':dict,
            'validate':list,
            'setup_hooks':list,
            'teardown_hooks':list
        }
        for key,value in template.items():
            if key in attrs and not isinstance(attrs[key],value):
                raise ValidationError(f'请传递正确的{key}格式：{value}')
        return attrs

# 用例
class CaseSerializer(serializers.ModelSerializer):
   # 模型中有的不符合的，可以更新它，模型中没有的可以创建（例如project_id），创建完的字段需要加在fields中返回
   # config字段为Config序列化器，REST会自动提取其值，创建case需要先创建config来关联，里面有case的name
   config=ConfigSerializer()
   # read_only=True:忽略字段，不作为入参处理; many=True:以列表形式展示; write_only=True:只做为入参
   teststeps=StepSerializer(required=False,many=True)
   project_id=serializers.CharField(write_only=True)
   create_by=UserSerializer(write_only=True,required=False)
   updated_by=UserSerializer(write_only=True,required=False)
   create_time=serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
   update_time=serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

   # 覆盖父类新增方法
   def create(self, validated_data):
       '''
       validated_data：校验后的入参-字典形式
       '''
       # 创建config
       config_kws=validated_data.pop('config')
       project=Project.objects.get(pk=validated_data.pop('project_id'))
       # 这里会有问题，如果用例没创建成功，config仍旧会被插入
       config=Config.objects.create(project=project,**config_kws)

       steps_kws=[]
       if 'teststeps' in validated_data:
           steps_kws=validated_data.pop('teststeps')

       # 创建用例
       file_path=f'{project.name}_{config.name}.json'
       # desc=validated_data.pop('desc')
       case=Case.objects.create(file_path=file_path,config=config,**validated_data)

       # 创建步骤
       if steps_kws:
           for steps_kw in steps_kws:
               steps_kw['belong_case_id']=case.id
               serializer=StepSerializer(data=steps_kw)
               if serializer.is_valid(raise_exception=True):
                   serializer.save()
       return case

   def update(self, instance, validated_data):
       '''
       :param instance:当前被修改的数据对象
       :param validated_data:校验后的入参--字典
       :return:
       '''
       config_kws=validated_data.pop('config')
       project=Project.objects.get(pk=validated_data['project_id'])
       # project = Project.objects.get(pk=validated_data.pop('project_id'))
       config_kws['project']=project
       # instance为case数据对象，调用config序列化器更新config数据
       conf_serializer=ConfigSerializer(instance=instance.config,data=config_kws)
       # 通过序列化器更新数据，反序列化（json-数据类型）需要校验：验证前端参数的正确性
       if conf_serializer.is_valid():
           conf_serializer.save()
       else:
           # 发生异常后保存在序列化器的error字段中
           raise ValidationError(conf_serializer.errors)

       #  teststeps更新，先删除所有step再去新增
       steps=instance.teststeps.all()
       for step in steps:
           step.delete()
       teststeps=validated_data.pop('teststeps')
       for step in teststeps:
           step['belong_case']=self.instance.id
           ss=StepSerializer(data=step)
           if ss.is_valid():
               ss.save()
           else:
               raise ValidationError(ss.errors)
       # python反射设值，validated_data不要包含instance数据对象没有的字段参数
       for k,v in validated_data.items():
           setattr(instance,k,v)
       # 要调用save方法
       instance.save()
       return instance

   def to_json_file(self,path=None):
       if path is None:
           path=self.instance.file_path
       if not path.endswith('json'):
           path=path+'json'

       # 生成的用例文件存放在项目目录的testcase目录下
       path=f'testcase/{path}'

       # 用例文件过滤输出参数
       valid_data=filter_data(self.data)
       # 生成json文件
       content=JSONRenderer().render(valid_data,accepted_media_type='application/json;indent=4')  # 获取文件内容--bytes
       with open(path,'wb') as f:
           f.write(content)
       return path

   class Meta:
       model=Case
       fields=['id','config','teststeps','project_id','file_path','desc','create_time','update_time','create_by','updated_by']

   def validate(self, attrs):
       template={
           'config':dict,
           'teststeps':list
       }
       for key,value in template.items():
           if key in attrs and not isinstance(attrs[key],value):
               raise ValidationError(f'请传递正确的{key}格式：{value}')
       return attrs

