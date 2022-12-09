from django.db import models

# Create your models here.

# 发布会模型-继承django自带的模型基类
class Event(models.Model):
    # 可不写id，django会自动创建一个自增长的id字段作为主键
    id=models.IntegerField(unique=True,primary_key=True)
    name=models.CharField(max_length=256,null=False)
    address=models.CharField(max_length=256,null=False)
    limits=models.IntegerField(default=100)
    status=models.BooleanField(default=True)
    startTime=models.DateTimeField(null=True)
    createTime=models.DateTimeField(null=True,auto_now_add=True) # auto_now_add创建时插入当前时间，固定不更新
    updateTime=models.DateTimeField(null=True,auto_now=True)  # auto_now，每次修改model都会更新

    # 修改模型自带方法 __str__ 调用该对象自动返回对象的name值
    def __str__(self):
        return self.name

class Guest(models.Model):
    # 外键定义在多方
    # event=models.ForeignKey(Event,on_delete=models.CASCADE) # 如果删除了Event，该Guest也会被删除
    # 改成多对多关系，如果有中间表，需要手动指定
    events=models.ManyToManyField(Event, through='GuestEvent')
    name=models.CharField(max_length=64,unique=True)
    phone=models.CharField(max_length=64,unique=True)
    email=models.EmailField()
    createTime=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GuestEvent(models.Model):
    # 通过外键关联对应的数据
    # 当关联的发布会或者嘉宾任意一个被删除，这条对应 关系也就不存在了
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    guest=models.ForeignKey(Guest,on_delete=models.CASCADE)
    join_time=models.DateTimeField(auto_now_add=True)
    is_sgin=models.BooleanField(default=False)

    # 修改下表名
    class Meta:  # 元类，用于设置模型元信息：表名...
        db_table='sgin_guest_events'