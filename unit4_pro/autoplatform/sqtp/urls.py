# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2022/12/22 10:06
@file:urls.py
@desc:
'''

from django.urls import path,include
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns
from sqtp import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view=get_schema_view(
    openapi.Info(
        title='SQTP API DOC',
        default_version='v1',
        description='SQTP接口文档',
        terms_of_service='https://www.baidu.com',
        contact=openapi.Contact(email='592902307@qq.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

# 使用rest框架自带的路由器生成路由列表
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
# 将视图信息注册路由列表
router.register(r'requests',views.RequestViewSet),
router.register(r'cases',views.CaseViewSet)
router.register(r'steps',views.StepViewSet)

urlpatterns=[
    # 类视图的调用，需要调用as_view方法
    # path('requests/',views.RequestList.as_view()),
    # path('requests/<int:_id>',views.RequestDetail.as_view())
    # 使用python定义好的视图，需要使用它本身自带的参数，所以要改成pk
    # path('requests/<int:pk>',views.RequestDetail.as_view())

    # 自动生成路由列表需要改成path('',include(router.urls))
    path('',include(router.urls)),
    path('users/',views.user_list),
    path('users/<int:_id>',views.user_detail),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/',schema_view.with_ui('redoc',cache_timeout=0),name='redoc-ui')
]
# 使用基于类的视图，要重写路由
# urlpatterns=format_suffix_patterns(urlpatterns)

