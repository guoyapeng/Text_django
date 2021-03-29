from abc import ABC

from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.throttling import SimpleRateThrottle


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
