from rest_framework.pagination import PageNumberPagination, CursorPagination


class CustomPagination(PageNumberPagination):
    # 此设置是指 通过url的参数size可以指定页面大小
    page_size_query_param = 'size'
    max_page_size = 50


class AgentCursorPagination(CursorPagination):
    """经理人游标分页类"""
    page_size_query_param = 'size'
    max_page_size = 50
    ordering = '-agentid'  # 按照经理人编号的降序排序
