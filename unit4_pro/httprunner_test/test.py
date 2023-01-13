# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/1/13 14:53
@file:test.py
@desc:
'''

import os
print(__file__)
print(os.path.realpath(__file__))
print(os.path.split(os.path.realpath(__file__ ))[0])
project_path=os.path.split(os.path.realpath(__file__ ))[0].split('configs')[0]
print(project_path)