from abc import ABC

from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response
from rest_framework.throttling import SimpleRateThrottle
from django_filters import filterset

from common.models import Estate


class CustomThrottle(SimpleRateThrottle):
    """重写父类方法，自定义限流策略"""
    scope = 'foo'

    def get_cache_key(self, request, view):
        return request.method  # 返回限流缓存key


class CustomPagination(PageNumberPagination):
    # 此设置是指 通过url的参数size可以指定页面大小
    page_size_query_param = 'size'
    max_page_size = 50


class AgentCursorPagination(CursorPagination):
    """经理人游标分页类"""
    page_size_query_param = 'size'
    max_page_size = 50
    ordering = '-agentid'  # 按照经理人编号的降序排序


class EstateFilterSet(filterset.FilterSet):
    """重写父类方法，自定义筛选方式"""
    name = filterset.CharFilter(lookup_expr='startswith')
    minhot = filterset.NumberFilter(field_name='hot', lookup_expr='gte')
    maxhot = filterset.NumberFilter(field_name='hot', lookup_expr='lte')
    dist = filterset.NumberFilter(field_name='district')

    class Meta:
        # 指定哪一个模型做筛选
        model = Estate
        # 指定根据哪些字段搜索
        fields = ('name', 'minhot', 'maxhot', 'dist')


class IZFResponse(Response):
    def __init__(self, code=10000, message='操作成功', data=None, status=None,
                 template_name=None, headers=None, exception=False, content_type=None):
        _data = {'code': code, 'message': message}
        if data:
            _data.update(data)
        super().__init__(_data, status, template_name, headers, exception, content_type)
