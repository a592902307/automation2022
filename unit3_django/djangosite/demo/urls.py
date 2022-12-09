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

urlpatterns = [
    path('index/',views.index),
]
