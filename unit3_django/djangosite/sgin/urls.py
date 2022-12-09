# encoding: utf-8
'''
@anthor:yh
@contact:592902307@qq.com
@time:2022/11/17 11:54
@file:urls.py
@desc:
'''

from django.urls import path,include
from . import views

# 子路由列表
urlpatterns = [
    # 发布会
    path('events/',views.events),
    # 发布会详情
    path('events/detail/<int:event_id>',views.event_detail),
    # 嘉宾
    path('guests/',views.guests),
    # 嘉宾详情
    path('guests/detail/<int:guest_id>',views.guest_detail),
    # 签到
    path('do_sgin/<int:event_id>',views.do_sign),
    # 签到成功页
    path('sgin_success/<int:phone>',views.sgin_success_page),
    # 添加发布会
    path('add_event_page/',views.add_event_page),
    path('add_event/',views.add_event),
    # 添加嘉宾
    path('add_guest_page/',views.add_guest),
    path('add_guest/',views.add_guest)
]
