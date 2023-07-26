# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/7/4 23:50
@file:task.py
@desc:
'''

from rest_framework import serializers
from sqtp.models import Plan,Report,User,Environment,Case
from sqtp.serializers import EnvironmentSerializer,UserSerializer,CaseSerializer

class PlanSerializer(serializers.ModelSerializer):
    case_ids=serializers.PrimaryKeyRelatedField(queryset=Case.objects.all(),many=True,required=False,write_only=True)
    cases=CaseSerializer(read_only=True,many=True)
    status=serializers.SerializerMethodField()
    environment_id=serializers.IntegerField(write_only=True,required=False)
    environment=EnvironmentSerializer(read_only=True,required=False)
    executor_id=serializers.IntegerField(write_only=True)
    executor=UserSerializer(read_only=True)

    create_by=UserSerializer(write_only=True,required=False)
    updated_by=UserSerializer(write_only=True,required=False)
    create_time=serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)
    update_time=serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)

    def get_status(self,obj):
        return obj.get_status_display()

    def validate(self, attrs):
        executor_id=attrs.get('executor_id', 0)
        if not User.objects.filter(pk=executor_id).count():
            raise serializers.ValidationError(f'请传入正确的executor_id:{executor_id}')
        environment_id=attrs.get('environment_id', 0)
        if not Environment.objects.filter(pk=environment_id).count():
            raise serializers.ValidationError(f'请传入正确的environment_id:{environment_id}')

        return attrs

    def update(self, instance, validated_data):
        '''
        :param instance: 当前被修改的数据对象
        :param validated_data: 校验后的入参（字典格式）
        :return:
        '''
        # 关联case
        case_ids=validated_data.pop('case_ids') # 取出关联的case对象
        instance.cases.set(case_ids) # 多对多关系关联
        # 设置属性-反射
        for k,v in validated_data.items():
            setattr(instance,k,v)
        instance.save()
        return instance

    class Meta:
        model=Plan
        fields=['case_ids','cases','id','name','desc','status','exec_counts','environment','executor','create_time','update_time','environment_id','executor_id','create_by','updated_by']

class ReportSerializer(serializers.ModelSerializer):
    plan=PlanSerializer(read_only=True)
    trigger=UserSerializer(read_only=True)
    create_time=serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)
    update_time=serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)

    class Meta:
        model=Report
        fields=['id','plan','trigger','detail','create_time','update_time','path']