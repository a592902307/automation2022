# -*-coding:utf-8 -*-
from django.conf.locale import cs
from django.db import transaction
from django.shortcuts import render,redirect

# Create your views here.

from django.http import HttpResponse
from sgin.models import Event,Guest,GuestEvent
from django.views.decorators.csrf import csrf_exempt

def events(request):
    # 从数据库读取数据
    event_list=Event.objects.all()

    # 简单的返回字符串
    # res=''.join([f'<li>{event}</li>' for event in event_list])
    # return HttpResponse([f'<li>{event}</li>' for event in event_list])
    # 返回模板
    return render(request,'events.html',{'event_list':event_list})

def event_detail(request,event_id):
    try:
        event=Event.objects.get(id=event_id)
    except:
        event=''
        # return render(request,'404.html')
    return render(request,'event_detail.html',{'event':event})

def guests(request):
    guest_list=Guest.objects.filter()
    return render(request,'guests.html',{'guest_list':guest_list})

def guest_detail(request,guest_id):
    try:
        guest=Guest.objects.get(id=guest_id)
    except:
        guest=''
        # return render(request,'404.html')
    return render(request,'guest_detail.html',{'guest':guest})

# 处理签到，csrf_exempt处理csrf跨域攻击
@csrf_exempt
def do_sign(request,event_id):
    # 获取待签到的发布会
    event=Event.objects.get(id=event_id)
    # event=Event.objects.filter(pk=event_id) # pk代表主键
    # 通过手机号获取签到嘉宾
    if request.method=="POST":
        phone=request.POST['phone']
        # 判断手机号是否存在表中
        res=Guest.objects.filter(phone=phone)
        if not res:
            return render(request,'event_detail.html',{"error":"手机号错误","event":event})
        guest=res[0]
        # 判断当前发布会是否是嘉宾所属的发布会
        event_list=guest.events.all()
        if event not in event_list:
            return render(request,'event_detail.html',{"error":"非当前发布会嘉宾","event":event})
        # 判断是否已经签到
        ge=GuestEvent.objects.get(guest_id=guest.id,event_id=event.id)
        if ge.is_sgin:
            return render(request,'event_detail.html',{"error":"已签到，不要重复提交","event":event})
        # 执行签到
        try:
            ge.is_sgin=True
            ge.save()
        except:
            return render(request,'event_detail.html',{"error":"签到失败，服务器异常","event":event})

        # 重定向
        return redirect(f'/sgin/sgin_success/{phone}')

def sgin_success_page(request,phone):
    return render(request,'sgin_success.html',{"phone":phone})

def add_event_page(request):
    return render(request,'event_add.html')
# 创建发布会
@csrf_exempt
def add_event(request):
    if request.method=="POST":
        name=request.POST['name']
        address=request.POST['address']
        limits=request.POST['limits']
        if request.POST.get('status',False):
            status=True
        else:
            status=False
        startTime=request.POST['startTime']
        try:
            event=Event.objects.create(name=name,address=address,limits=limits,status=status,startTime=startTime)
        except Exception as e:
            return render(request,'event_add.html',{'error':repr(e)})
        return redirect('sgin/events/')

# 创建嘉宾
@csrf_exempt
def add_guest(request):
    if request.method=="GET":
        event_list=Event.objects.all()
        return render(request,'guest_add.html',{'events':event_list})
    if request.method=="POST":
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        # 关联发布会，获取值的列表
        event_ids = request.POST.getlist('event_ids')
        try:
            # 事务：创建嘉宾+关联发布会
            with transaction.atomic():
                guest=Guest.objects.create(name=name,phone=phone,email=email)
                # 在中间表增加关联关系
                event_list=[Event.objects.get(pk=event_id) for event_id in event_ids]
                guest.events.add(*event_list) # 添加
                # guest.events.set(event_list)  # 覆盖添加
        except Exception as e:
            return render(request,'guest_add.html',{'error':repr(e)}) # repr返回精简的错误信息
        return redirect('/sgin/guests/')
