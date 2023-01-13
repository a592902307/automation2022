# encoding: utf-8
'''
@anthor:yh
@contact:592902307@qq.com
@time:2022/12/13 16:59
@file:debugtalk.py
@desc:
'''
'''
1、约定：项目有且只有一个debugtalk.py
2、函数：测试用例中引用到的函数在此定义
3、在这里可以读取数据库，调用接口，返回数据给用例使用
'''
import json
import requests

def login_variables():
    return {'account':'auto','psw':'sdfsdfsdf','code':0}

def add_course_variables():
    return [
        {"name":"大学数学1","desc":"微积分","idx":"20"},
        {"name":"大学数学2","desc":"高等数学","idx":"21"},
    ]

def setup_case():
    with open('setup.txt', 'w', encoding='utf-8') as f:
        f.write('执行初始化')

def teardown_case():
    with open('teardown.txt', 'w', encoding='utf-8') as f:
        f.write('执行清除步骤')

def delete_course(response,sessionid):
    # 从返回的response提取到id
    id=response.json['id']
    url='http://localhost/api/mgr/sq_mgr/'
    payload={
        "action":"delete_course",
        "id":id
    }
    cookies={
        "sessionid":sessionid
    }
    res=requests.delete(url=url,data=payload,cookies=cookies)
    return res.json()
