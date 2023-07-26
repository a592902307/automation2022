# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2022/12/26 17:35
@file:renderers.py
@desc:
'''

from rest_framework.renderers import JSONRenderer
# 自定义渲染器
class MyRenderer(JSONRenderer):
    # 重构 render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # renderer_context：view,request,response,args,kwargs 是一个由view提供的上下文信息的字典。
        print(renderer_context)
        print(renderer_context['response'])
        # 响应状态码，正常返回 status_code 以2开头
        status_code=renderer_context['response'].status_code
        if str(status_code).startswith('2'):
            # 预设返回模板
            res={'msg':'success','retcode':status_code}
            if not isinstance(data,list):
                if 'retlist' not in data:
                    res.update({'retlist':[data]})
                else:
                    res.update(data)
            else:
                res.update({'retlist':data})
            # 返回父类方法
            return super().render(res,accepted_media_type,renderer_context)
        else:
            # 异常情况交给exception自定义异常去处理
            return super().render(data,accepted_media_type,renderer_context)

