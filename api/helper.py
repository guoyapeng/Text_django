from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    # 此设置是指 通过url的参数size可以指定页面大小
    page_size_query_param = 'size'
    max_page_size = 50
