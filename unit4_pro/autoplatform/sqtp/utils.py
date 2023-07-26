# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/5/29 23:02
@file:utils.py
@desc:
'''

# 自定义模板匹配方法
import os


def filter_data(data):
    template = {
        'config': {
            'name': str,
            'base_url': str,
            'variables': dict,
            'parameters': dict,
            'verify': bool,
            'export': list
        },
        'teststeps': [{
            'name': str,
            'variables': list,
            'extract': dict,
            'validate': list,
            'setup_hooks': list,
            'teardown_hooks': list,
            'request': {
                'method': str,
                'url': str,
                'params': list,
                'headers': dict,
                'cookies': dict,
                'data': dict,
                'json': dict
            },
        }]
    }
    return merge_dict(template,data)

def merge_dict(left,right):
    for k in right:
        if k in left:
            if isinstance(left[k],dict) and isinstance(right[k],dict):
                merge_dict(left[k],right[k])
            elif isinstance(left[k],list) and isinstance(right[k],list):
                for one in right[k]:
                    merge_dict(left[k][0],one)
            elif right[k]:
                left[k]=right[k]
            elif not right[k]:
                left.pop(k)
    for k in list(left.keys()):
        if k not in right:
            left.pop(k)
    return left

# 执行前清空用例目录中现有的内容
def setup_case_dir(case_path):
    empty_dir_files(case_path,'json','pyc','py')

def empty_dir_files(path,*suffix):
    # root:原路径  dirs:该路径下的文件夹  files:该路径下的文件
    for root,dirs,files in os.walk(path):
        for fi in files:
            if fi.split('.')[-1] in suffix:
                print(os.path.join(root,fi))
                os.remove(os.path.join(root,fi))

# 执行前清空logs中现有的内容
def setup_logs_dir(log_path):
    empty_dir_files(log_path,'log')

def collect_log(path):
    content_list=[]
    for fi in os.listdir(path):
        with open(f'{path}/{fi}') as f:
            content_list.append(f.read())
    return '\n'.join(content_list)