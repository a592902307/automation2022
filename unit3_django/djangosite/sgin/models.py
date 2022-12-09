from django.db import models

# Create your models here.

# ������ģ��-�̳�django�Դ���ģ�ͻ���
class Event(models.Model):
    # �ɲ�дid��django���Զ�����һ����������id�ֶ���Ϊ����
    id=models.IntegerField(unique=True,primary_key=True)
    name=models.CharField(max_length=256,null=False)
    address=models.CharField(max_length=256,null=False)
    limits=models.IntegerField(default=100)
    status=models.BooleanField(default=True)
    startTime=models.DateTimeField(null=True)
    createTime=models.DateTimeField(null=True,auto_now_add=True) # auto_now_add����ʱ���뵱ǰʱ�䣬�̶�������
    updateTime=models.DateTimeField(null=True,auto_now=True)  # auto_now��ÿ���޸�model�������

    # �޸�ģ���Դ����� __str__ ���øö����Զ����ض����nameֵ
    def __str__(self):
        return self.name

class Guest(models.Model):
    # ��������ڶ෽
    # event=models.ForeignKey(Event,on_delete=models.CASCADE) # ���ɾ����Event����GuestҲ�ᱻɾ��
    # �ĳɶ�Զ��ϵ��������м����Ҫ�ֶ�ָ��
    events=models.ManyToManyField(Event, through='GuestEvent')
    name=models.CharField(max_length=64,unique=True)
    phone=models.CharField(max_length=64,unique=True)
    email=models.EmailField()
    createTime=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GuestEvent(models.Model):
    # ͨ�����������Ӧ������
    # �������ķ�������߼α�����һ����ɾ����������Ӧ ��ϵҲ�Ͳ�������
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    guest=models.ForeignKey(Guest,on_delete=models.CASCADE)
    join_time=models.DateTimeField(auto_now_add=True)
    is_sgin=models.BooleanField(default=False)

    # �޸��±���
    class Meta:  # Ԫ�࣬��������ģ��Ԫ��Ϣ������...
        db_table='sgin_guest_events'